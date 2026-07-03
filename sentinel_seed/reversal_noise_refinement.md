# PR #92: tune: raise Celery worker prefetch and add index on orders.created_at

**Author:** @daniel-osei
**Branch:** tune-workers → main

## Description

Two small performance refinements, both consistent with how the system already works: give the queue workers a higher prefetch so the email backlog drains faster after bursts, and index `orders.created_at` for the ops dashboard's date-range queries.

## Diff

```diff
--- a/email_service/worker.py
+++ b/email_service/worker.py
@@
-app.conf.worker_prefetch_multiplier = 1
+app.conf.worker_prefetch_multiplier = 4  # drain bursts faster

--- a/migrations/0044_orders_created_idx.py
+++ b/migrations/0044_orders_created_idx.py
@@
+migrations.AddIndex("Order", models.Index(fields=["created_at"]))
```
