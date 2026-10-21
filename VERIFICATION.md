# Verification notes — 21 October 2026

## Parser regression

Command: `python -m unittest discover -s tests -v` from the repository root.

Before the change: five test methods ran; the existing-list test raised ValueError for empty and multi-element lists. After the change: all five test methods passed. The fix moves the existing-list check ahead of pandas null checking and preserves the prior return behaviour for valid lists and serialised lists.

Tests cover existing lists, serialised lists and whitespace, missing scalar values, malformed/non-list inputs, and code-like text without execution. The tests use unittest from Python's standard library and the existing pandas dependency.

## Reproduction limits

The workbook `data/job_postings_monthly.xlsx` is absent, so the full aggregation pipeline was not rerun and Power BI refresh was not tested. The supplied role-summary counts total 52,924; their weighted remote proportion is approximately 13.8%. Those are internal consistency checks of saved summaries, not independent verification against the source.

The original PBIX, PDF, screenshots, CSV summaries, requirements and data dictionary were preserved byte-for-byte. No dataset or licence was added. Small replacement datasets may expose the existing assumption that at least one skill reaches the 500-occurrence threshold; that aggregation path is outside the parser fix.

Parser tests ran with Python 3.12.14 and pandas 2.2.3. These are observed review versions, not a replacement dependency lock.
