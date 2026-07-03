# PR #89: chore: bump celery 5.3.6 → 5.4.0 and requests to latest patch

**Author:** @dependabot
**Branch:** deps-celery-5.4 → main

## Description

Routine dependency maintenance. Celery 5.4.0 is a compatible minor release (changelog: logging fixes, Python 3.12 support). Requests patch bump picks up a CVE fix. No code changes.

## Diff

```diff
--- a/requirements.txt
+++ b/requirements.txt
@@
-celery==5.3.6
+celery==5.4.0
-requests==2.31.0
+requests==2.32.3
```
