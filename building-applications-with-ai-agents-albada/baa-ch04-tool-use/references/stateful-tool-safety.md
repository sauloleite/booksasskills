# Stateful tool safety

Stateful tools touch data that persists and changes: databases, files, tickets, accounts. They can be local, API-based or MCP-hosted; the risk is the same. Giving a model write power over live state lets it make destructive mistakes or be steered into them by an attacker. The chapter cites a real case where an agent "optimizing" a database deleted about half the rows of a production table. No malice is needed: a misread intent can turn a lookup into a destructive command.

## Principle of least power

Expose the smallest toolset the task truly requires, and put a precise boundary and oversight on every operation. Concretely:

1. Narrow operations, not general endpoints. Replace "execute SQL" with tools such as `get_order(order_id)` or `create_customer(record)`, each wrapping one tested query or procedure.
2. Separate read from write. An agent that only needs to read gets no tools that modify or delete.
3. Least privilege below the tool. The credential behind each tool carries just the permissions its permitted operations need.
4. Constrain at registration. What is not registered cannot be called, which shrinks both the attack surface and the blast radius of errors.

## When free-form queries cannot be avoided

- Sanitize: OWASP's GenAI Security Project warns that prompt injection can smuggle clauses such as DROP or ALTER into innocent-looking requests. Reject any statement matching destructive patterns.
- Always use parameter binding or prepared statements; never interpolate model text into SQL.
- Run under a restricted account (read-only role, limited schemas, row limits).

Illustrative guard (a deny-list is a backstop, not a substitute for narrow tools):

```python
import re
BLOCKED = re.compile(r"\b(drop|alter|truncate|delete|update|insert|grant|create)\b", re.I)

def guarded_select(sql: str, params: tuple, conn):
    if not sql.lstrip().lower().startswith("select") or BLOCKED.search(sql) or ";" in sql.rstrip(";"):
        raise PermissionError("only single parameterized SELECT statements are allowed")
    return conn.execute(sql, params).fetchmany(500)
```

## Observability and response

- Log every tool invocation (caller, arguments, result size, latency) for anomaly detection and forensics.
- Alert in real time on suspicious patterns: unusually large deletions, schema-changing commands, bursts of writes, access outside normal scopes.
- Fast alerts let a human step in before a small error cascades into an incident.

## Review checklist before registering a stateful tool

- [ ] Does each tool perform one well-defined, tested operation?
- [ ] Does any tool accept raw SQL, shell, code or a URL the model controls? If yes, is it justified and sanitized?
- [ ] Are read and write capabilities split, and does each agent get only the side it needs?
- [ ] Does the backing credential have minimal privileges?
- [ ] Are inputs schema-validated and parameter-bound?
- [ ] Is every call logged, with alerts on destructive or high-volume actions?
- [ ] Do irreversible actions require confirmation or human approval?

The same safeguards apply whether the tool is local, behind an API or on an MCP server: restrict capability, sanitize input, enforce least privilege, keep full observability.
