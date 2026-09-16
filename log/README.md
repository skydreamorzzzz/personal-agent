# Runtime logs

This directory is reserved for machine-generated runtime logs, diagnostics, and
structured traces. Runtime files under `log/runtime/` and common log/JSONL files
are ignored by Git.

Logs must never contain API keys, credentials, secret file contents, or an
unredacted sensitive payload. A future structured logger should record event type,
time, task/run identity, and safe metadata, with redaction before persistence.
