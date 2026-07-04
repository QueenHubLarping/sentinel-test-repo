# PR #87: Handle provider callbacks in the request — remove the handoff indirection

**Author:** @new-contributor
**Branch:** inline-callbacks → main

## Description

Tracing a callback today means hopping from the endpoint to a stored row to a background worker to the actual logic. This PR does the work right in the view: when the provider calls us, we update the order and write the ledger entry before responding. One stack trace, no indirection, easier debugging.

## Diff

```diff
--- a/webhooks/views.py
+++ b/webhooks/views.py
@@ def provider_callback(request):
     verify_signature(request)
-    RawEvent.objects.create(payload=request.body)
-    return Response(status=204)  # worker picks it up from here
+    event = parse_event(request.body)
+    apply_order_transition(event)      # do it now, in-request
+    write_ledger_entry(event)
+    notify_customer(event)
+    return Response(status=200)

--- a/webhooks/tasks.py
+++ b/webhooks/tasks.py
@@
-@queue.task
-def process_raw_event(event_id):
-    ...
```
