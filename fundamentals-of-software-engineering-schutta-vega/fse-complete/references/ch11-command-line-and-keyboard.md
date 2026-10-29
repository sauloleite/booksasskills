# Command Line and Keyboard Fluency

Covers: Leverage the Power of the Command Line, Harness the Power of Keyboard Shortcuts, Emacs Versus vi (sidebar), clipboard history and text expansion.

## Contents
- Why the CLI matters
- Composition with pipes
- Modern replacements for classic commands
- Aliases: when they help and when they hurt
- Shell history and fuzzy finding
- Alternative shells
- Keyboard-first work and touch typing
- Shortcut layers to learn
- Emacs bindings and vi basics
- Clipboard history and text expanders
- Pitfalls

## Why the CLI matters

GUIs are welcome, but an engineer must also be at ease in a terminal. Many routine jobs take a few keystrokes there versus many clicks elsewhere, so CLI skill compounds over a career. Habit to build: a few minutes each week trying commands not yet used. When unsure what a command does, consult its manual page (`man <command>`) before searching the web.

## Composition with pipes

The core idea: chain small single-purpose tools with `|` to produce answers none of them gives alone. Useful building blocks beyond `cd/ls/pwd/mkdir`: `open` (launch apps or files on macOS), `cat`, `grep`, `cut`, and clipboard commands (`pbcopy` on macOS; `xclip` or `wl-copy` on Linux; `clip` on Windows). Original illustration:

```sh
# Ten most frequent error lines in a log, copied to the clipboard
grep -i error app.log | sort | uniq -c | sort -rn | head -10 | pbcopy

# Which branches did I touch most recently?
git for-each-ref --sort=-committerdate refs/heads --format='%(refname:short)' | head -5
```

Even modest regex knowledge makes these pipelines far more powerful.

## Modern replacements for classic commands

| Classic | Upgrade the book points to | Benefit |
|---|---|---|
| `cat` | `bat` | Syntax highlighting |
| `diff` / git diff | diff-so-fancy | Readable diffs |
| raw JSON in terminal | `fx` | Interactive JSON viewing |
| `ls` | `exa` (its maintained fork today is `eza`) | Color and better formatting |

Also: macOS `say` can make the machine speak, handy for signalling that a long job finished.

## Aliases: when they help and when they hurt

Define aliases in the shell config (`~/.bashrc`, `~/.zshrc`) for commands that are frequent or long to type, e.g. a one-letter alias for a container or cluster CLI. Trade-off: muscle memory built on aliases fails on servers, containers or colleagues' machines that lack them. Rule: alias only high-frequency or verbose commands, and still know the underlying full command.

## Shell history and fuzzy finding

History is one of the most undervalued CLI features:
- Arrow keys to scroll back; Tab completion; `history` to list past commands; Ctrl-R for reverse incremental search.
- It is configurable: larger history size, ignoring noisy or sensitive commands.
- Adding a fuzzy finder (fzf is a common choice) to history search means a long command rarely needs retyping.

## Alternative shells

Do not assume the OS default shell is the end state. Frameworks such as Oh My Zsh bundle helper functions plus thousands of plug-ins and themes.

## Keyboard-first work and touch typing

- Goal: hands stay on the home row (the resting row, located by the tactile bumps under the index fingers). Shortcuts are faster than pointer trips and reduce wrist and hand strain.
- Touch typing is non-negotiable in the authors' view. Thumb typing on phones does not transfer; gamified online trainers make learning painless. Benefits extend to hands, eyes and neck.
- Shortcut mastery is a visible marker separating novices from experienced engineers.

## Shortcut layers to learn

1. Editor/IDE shortcuts (navigation, refactoring, run/test). Example class: IntelliJ can diff any two selected files, including archive files like JARs and ZIPs.
2. Operating system shortcuts (window management, hiding the front app, showing all windows of an app; on macOS, Cmd-H and Ctrl-Down respectively).
3. Text navigation bindings that work across many apps (next section).

Learn them incrementally; one per week is the chapter's suggested cadence.

## Emacs bindings and vi basics

Many apps and OS text fields honor Emacs-style movement:

| Action | Binding |
|---|---|
| Char forward / back | Ctrl-F / Ctrl-B |
| Word forward / back | Meta-F / Meta-B (Meta is often Alt, sometimes Esc or Caps Lock) |
| Line start / end | Ctrl-A / Ctrl-E |

Note: the book's text swaps the line-start and line-end keys; the table above is the standard mapping.

The editor wars are notoriously heated, so do not pick fights over them. Practical guidance: learn enough vi to open, edit, save and quit, because on a bare server it may be the only editor present; learn a handful of Emacs bindings for fast text navigation everywhere.

## Clipboard history and text expanders

- Clipboard managers (Pastebot is the book's example) keep a paste history, letting someone copy several items from one window and paste them all in another without bouncing back and forth, and recover something copied hours earlier. Caution: the history can retain passwords and secrets; exclude password managers or clear history.
- Text expanders (dedicated apps or the OS's built-in text replacement) turn short triggers into long snippets: email signatures, boilerplate, commit trailers. Each saves seconds; the savings accumulate.

## Pitfalls

- Relying on aliases you cannot reproduce elsewhere.
- Clipboard history leaking secrets.
- Learning too many shortcuts at once and retaining none.
- Treating editor choice as identity; prioritize team compatibility.
