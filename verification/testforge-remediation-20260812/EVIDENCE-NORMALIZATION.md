# Evidence normalization

Captured command streams are stored as UTF-8 with LF line endings and trailing line whitespace removed. Exit codes, timestamps, command arguments, substantive stdout/stderr text, and failure classifications are unchanged. This normalization prevents shell-formatting noise from violating repository whitespace policy; it is not evidence that the commands were rerun or that their results changed.
