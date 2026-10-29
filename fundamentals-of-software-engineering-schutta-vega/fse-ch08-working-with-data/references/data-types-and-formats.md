## Contents

- Five questions before picking a representation
- Structured versus unstructured data
- Interchange format selection (JSON, XML, CSV, YAML)
- Specialized data: binary, date and time, large datasets
- Practice drills

# Data Types and Formats

## Five questions before picking a representation

Ask these before choosing a shape or a wire format, and write the answers down in the design note or PR description:

1. **Who consumes it?** People editing by hand, or programs parsing it?
2. **Do bytes or parse time matter?** Payload size and processing speed may dominate.
3. **Which systems must read it?** Existing partners, tools or platforms often decide for you.
4. **How deep and how variable is the shape?** Flat rows, nested trees, optional sections.
5. **Must it be validated against a schema?** Contracts with external parties usually say yes.

## Structured versus unstructured data

| Aspect | Structured | Unstructured |
|---|---|---|
| Shape | Fixed schema; every record has the same fields and types | No model; free text, media, irregular logs, PDFs, Word files |
| Relationships | Explicit links between entities | Implicit, buried in content |
| Querying | Precise filters on any field | Needs full-text search, NLP, or computer vision |
| Storage | Columns in tables, compact | Large objects, specialized stores or data lakes |
| Typical domains | Payments, inventory, user profiles | Messages, reviews, chat transcripts, images, audio |
| Main weakness | Rigid: a new field touches schema and code; nested data is awkward | Hard to query and aggregate |

Decision guidance:

- Pick structured storage when integrity rules, complex queries and stable business rules matter. If you are on PostgreSQL or MySQL, the DDL is the contract.
- Unstructured content is where the nuance lives (tone, opinion, visual detail). Process it in a pipeline step that derives structured facts from it.
- **Hybrid pattern (recommended default for user-generated content):** keep the raw artifact, and next to it store structured metadata you extracted (sentiment label, keywords, language, owner, timestamps). Query on the metadata; keep the original for reprocessing when your extractors improve.

```python
def ingest_review(raw_text, analyzer, repo):
    facts = {
        "sentiment": analyzer.sentiment(raw_text),   # e.g. "negative"
        "topics": analyzer.topics(raw_text),         # e.g. ["shipping", "refund"]
    }
    repo.save(original=raw_text, **facts)            # keep raw + derived
```

**AI-assisted test data.** For a structured schema, an assistant can produce realistic fake rows quickly. Give it the schema, row count, output format and a domain flavor (for example "a used-camera shop" or "a running-club app"). Review the output for schema conformance before seeding.

## Interchange format selection

| Format | Strengths | Weaknesses | Default use |
|---|---|---|---|
| JSON | Readable, simple, language neutral; objects, arrays, strings, numbers, booleans, null | No comments, no native date type, binary only via encoding | Web APIs, document stores, config for JS-heavy stacks |
| XML | Strong validation (XSD, DTD), namespaces, XPath querying, XSLT transforms, streaming parsers for huge files | Verbose | Enterprise integration, document formats (DOCX, SVG), contracts needing schema validation |
| CSV | Tabular, tiny, opens in any spreadsheet | No types, inconsistent quoting and escaping rules | Exports, simple flat exchange |
| YAML | Comments, anchors and references, multiline strings, easy to read | Indentation is syntax; one stray space breaks parsing | Human-edited config: Compose, Kubernetes, CI pipelines |

Rules of thumb:

- A JavaScript front end or a public HTTP API means JSON unless something forces otherwise.
- Need schema validation, namespaces or compatibility with document-centric systems? Choose XML.
- Real systems mix formats: JSON on the API, YAML for deployment config, CSV for the "download my data" button. Do not force one format everywhere.
- Sometimes the format was chosen before you arrived. Your job is then to know its weak spots, not to relitigate it.

**CSV checklist** (configure the library explicitly, never rely on defaults):

- Empty fields versus missing columns
- Delimiters, quotes and line breaks inside values
- Character encoding and international text
- Type coercion on read (leading zeros in postal codes, dates, decimals)
- Flattening nested objects into dotted column names

**YAML checklist:** two-space indentation everywhere, validate or lint before deploying, edit with a YAML-aware editor, and watch implicit typing (unquoted values such as postal codes with leading zeros or `no` may not parse as strings).

## Specialized data

### Binary data

Images, documents, audio and encrypted blobs cannot be handled as text. Once loaded as bytes you can display, transform (resize, crop, filter), convert between image formats, upload, attach to HTTP requests, embed in PDFs or read metadata.

Practices:

- Use a library built for the specific file format instead of hand-parsing bytes.
- Base64-encode when binary has to travel inside JSON, XML or other text.
- Dump hex when debugging individual bytes.
- Stream or chunk large files; do not slurp a multi-gigabyte video into memory.
- Treat truncated or corrupt files as expected input and handle the errors.

### Date and time

Deceptively hard because of time zones, daylight-saving shifts, multiple calendars and formatting. Non-negotiables:

1. Persist instants in UTC; convert to a local zone only at the presentation edge.
2. Exchange timestamps between systems as ISO 8601 strings with an offset.
3. Use the platform's modern date/time library (java.time, Python zoneinfo, Temporal); never write your own arithmetic.
4. Show the zone explicitly in UIs whenever ambiguity is possible.

Worked example (invented): a flight leaves at 22:30 local in Sao Paulo and lasts 11h40m. Attach `America/Sao_Paulo` to the departure, convert to an instant, add the duration, then render in `Europe/Lisbon`. Adding hours to a naive local time silently breaks across DST changes.

### Large datasets

When data outgrows memory:

- Stream records one at a time (iterators, cursors, streaming parsers).
- Paginate API responses and UI lists.
- Index and tune queries in the database instead of filtering in the app.
- At extreme scale, evaluate data warehouses or distributed processing frameworks.
- Guard shared mutable state with locks, atomic operations or immutable structures when several threads process data concurrently.
- Load production-like volumes early; a 50-row dev table hides every scaling bug.

You are not expected to master all of this up front. The skill is noticing when the ordinary approach stops being enough and bringing in specialized tools or people.

## Practice drills

- Convert a messy CSV (quoted commas, blanks, accented names, leading-zero codes) into typed JSON and write tests for each edge case.
- Design storage for user-uploaded photos with captions: decide what is structured metadata, what is a blob, and how a search for "beach photos from 2024" would be served.
- Build a small tool that processes a multi-gigabyte log file with a streaming reader and bounded memory.
