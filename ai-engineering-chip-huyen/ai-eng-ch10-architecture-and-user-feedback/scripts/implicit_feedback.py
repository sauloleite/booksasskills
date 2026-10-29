#!/usr/bin/env python3
"""Aggregate implicit conversational feedback signals from a JSONL log.

Input: a JSONL file, one conversation per line:
  {"id": "c1",
   "turns": [{"role": "user", "text": "..."},
             {"role": "assistant", "text": "...", "stopped": true,
              "regenerated": false, "edited": false}, ...],
   "actions": ["delete" | "rename" | "share" | "bookmark", ...],
   "explicit": "up" | "down" | null}
Only "id" and "turns" are required. Assistant-turn flags default to false.

Signals per conversation (heuristic, keyword based, English only):
  early_stop     any assistant turn with stopped=true
  regenerate     any assistant turn with regenerated=true
  edit           any assistant turn with edited=true
  correction     a user turn after the first that opens with a negation or
                 restated intent ("no", "i meant", "that's not", "wrong", ...)
  rephrase       a user turn whose word-set Jaccard overlap with the previous
                 user turn is >= --rephrase-threshold
  confirm        user asks to verify or cite ("are you sure", "source", ...)
  refusal        assistant declines or claims ignorance
  negative       user message contains a frustration cue
  loop           user turns >= --long-turns and assistant distinct-token
                 ratio < --min-diversity

Output: per-conversation rows (with --per-conversation) and an aggregate
summary: share of conversations with each signal, mean user turns, mean
assistant diversity, organization action counts, explicit up/down counts.
Use --json for machine-readable output. Deterministic, stdlib only.

Example:
  python3 implicit_feedback.py conversations.jsonl --per-conversation
"""
import argparse
import json
import re
import sys
from collections import Counter

CORRECTION_STARTS = ("no", "nope", "i meant", "i mean", "that's not", "that is not",
                     "not what", "wrong", "actually", "incorrect")
CONFIRM_CUES = ("are you sure", "double check", "double-check", "check again",
                "source", "sources", "cite", "citation", "verify")
REFUSAL_CUES = ("i can't help", "i cannot help", "i'm unable", "i am unable",
                "as an ai", "as a language model", "i don't know", "i do not know",
                "i'm not able", "i am not able")
NEGATIVE_CUES = ("ugh", "useless", "annoying", "frustrat", "terrible", "awful",
                 "waste of time", "not helpful", "stupid", "ridiculous")
SIGNALS = ("early_stop", "regenerate", "edit", "correction", "rephrase",
           "confirm", "refusal", "negative", "loop")


def words(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def has_cue(text, cues):
    t = " ".join(words(text))
    return any(re.search(r"\b" + re.escape(c), t) for c in cues)


def starts_with(text, starts):
    t = " ".join(words(text))
    return any(t == s or t.startswith(s + " ") for s in starts)


def jaccard(a, b):
    a, b = set(words(a)), set(words(b))
    return len(a & b) / len(a | b) if a | b else 0.0


def analyze(conv, args):
    turns = conv.get("turns", [])
    users = [t.get("text", "") for t in turns if t.get("role") == "user"]
    bots = [t for t in turns if t.get("role") == "assistant"]
    bot_tokens = [w for t in bots for w in words(t.get("text", ""))]
    diversity = len(set(bot_tokens)) / len(bot_tokens) if bot_tokens else 1.0
    s = {
        "early_stop": any(t.get("stopped") for t in bots),
        "regenerate": any(t.get("regenerated") for t in bots),
        "edit": any(t.get("edited") for t in bots),
        "correction": any(starts_with(u, CORRECTION_STARTS) for u in users[1:]),
        "rephrase": any(jaccard(users[i - 1], users[i]) >= args.rephrase_threshold
                        for i in range(1, len(users))),
        "confirm": any(has_cue(u, CONFIRM_CUES) for u in users),
        "refusal": any(has_cue(t.get("text", ""), REFUSAL_CUES) for t in bots),
        "negative": any(has_cue(u, NEGATIVE_CUES) for u in users),
        "loop": len(users) >= args.long_turns and diversity < args.min_diversity,
    }
    return {"id": conv.get("id"), "user_turns": len(users),
            "assistant_diversity": round(diversity, 3),
            "actions": conv.get("actions", []), "explicit": conv.get("explicit"),
            "signals": s}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("log", help="JSONL file, one conversation per line ('-' for stdin)")
    p.add_argument("--rephrase-threshold", type=float, default=0.5,
                   help="Jaccard overlap between consecutive user turns that counts as a rephrase")
    p.add_argument("--long-turns", type=int, default=6, help="user turns at which a conversation is 'long'")
    p.add_argument("--min-diversity", type=float, default=0.4,
                   help="assistant distinct-token ratio below which a long conversation is a loop")
    p.add_argument("--per-conversation", action="store_true", help="print one row per conversation")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = p.parse_args()

    fh = sys.stdin if args.log == "-" else open(args.log, encoding="utf-8")
    rows = [analyze(json.loads(line), args) for line in fh if line.strip()]
    n = len(rows)
    if n == 0:
        sys.exit("no conversations found")
    rates = {k: sum(r["signals"][k] for r in rows) / n for k in SIGNALS}
    summary = {
        "conversations": n,
        "signal_rates": {k: round(v, 3) for k, v in rates.items()},
        "mean_user_turns": round(sum(r["user_turns"] for r in rows) / n, 2),
        "mean_assistant_diversity": round(sum(r["assistant_diversity"] for r in rows) / n, 3),
        "actions": dict(sorted(Counter(a for r in rows for a in r["actions"]).items())),
        "explicit": dict(sorted(Counter(r["explicit"] for r in rows if r["explicit"]).items())),
    }
    if args.json:
        out = {"summary": summary}
        if args.per_conversation:
            out["conversations"] = rows
        print(json.dumps(out, indent=2))
        return
    if args.per_conversation:
        for r in rows:
            fired = ",".join(k for k in SIGNALS if r["signals"][k]) or "-"
            print(f"{r['id']}: turns={r['user_turns']} div={r['assistant_diversity']} "
                  f"signals={fired} actions={','.join(r['actions']) or '-'} explicit={r['explicit']}")
        print()
    print(f"Conversations: {n}")
    for k in SIGNALS:
        print(f"  {k:<11} {rates[k]:6.1%}")
    print(f"Mean user turns: {summary['mean_user_turns']}")
    print(f"Mean assistant diversity: {summary['mean_assistant_diversity']}")
    print(f"Actions: {summary['actions']}")
    print(f"Explicit: {summary['explicit']}")
    print("Note: signals are context dependent (share, regenerate, length); combine them before judging.")


if __name__ == "__main__":
    main()
