# PR #85: Simplify database config — connect workers straight to the database

**Author:** @new-contributor
**Branch:** remove-db-proxy → main

## Description

We run an extra proxy container between the app and the database. It's one more thing to deploy, monitor, and debug through — and prepared statements need a workaround in its transaction mode. This PR removes the middleman: workers talk to the database directly, which is simpler and shaves a network hop.

## Diff

```diff
--- a/config/settings.py
+++ b/config/settings.py
@@ DATABASES = {
-        "HOST": "pgbouncer",
-        "PORT": 6432,
+        "HOST": "postgres",
+        "PORT": 5432,
+        "CONN_MAX_AGE": 600,  # keep connections warm per worker

--- a/docker-compose.yml
+++ b/docker-compose.yml
@@ services:
-  pgbouncer:
-    image: edoburu/pgbouncer:latest
-    volumes: [./infra/pgbouncer.ini:/etc/pgbouncer/pgbouncer.ini]
```
