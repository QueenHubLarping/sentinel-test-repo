# PR #84: Clean up the capture endpoint — remove the dedupe bookkeeping

**Author:** @another-contributor
**Branch:** simplify-capture → main

## Description

Integrators keep tripping over the mandatory header on the capture call — it's the top integration-support complaint. The extra table and unique index also add a write to our hottest path. This PR drops the requirement and the bookkeeping table; the endpoint just forwards the capture to the processor.

## Diff

```diff
--- a/payments/capture.py
+++ b/payments/capture.py
@@ def capture(request):
-    key = require_idempotency_key(request)
-    prior = IdempotencyRecord.objects.filter(key=key).first()
-    if prior:
-        return Response(prior.response_snapshot, status=prior.status_code)
     result = processor.capture(request.data["payment_id"], request.data["amount"])
-    IdempotencyRecord.objects.create(key=key, response_snapshot=result.json())
     return Response(result.json(), status=201)

--- a/payments/models.py
+++ b/payments/models.py
@@
-class IdempotencyRecord(models.Model):
-    key = models.CharField(max_length=64, unique=True)
-    response_snapshot = models.JSONField()
```
