# PR #86: Search the live product tables so results are always fresh

**Author:** @another-contributor
**Branch:** fresh-search → main

## Description

Merchandising noticed a product edit can take up to a minute to appear in search. Rather than tuning the copy pipeline, this PR queries the source-of-truth tables directly with the ORM — results are correct the instant anything changes, and we get to delete a background job.

## Diff

```diff
--- a/search/views.py
+++ b/search/views.py
@@ def search(request):
-    rows = SearchReadModel.objects.filter(text__search=q)
+    rows = (Product.objects
+        .select_related("pricing", "inventory", "brand")
+        .prefetch_related("categories__tree", "variants__options")
+        .filter(name__icontains=q))
     return Response(serialize(rows))

--- a/jobs/sync_read_model.py
+++ b/jobs/sync_read_model.py
@@
-def sync_read_model(event):
-    ...
```
