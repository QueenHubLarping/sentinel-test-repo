# PR #90: fix: handle missing shipping address in order summary

**Author:** @new-contributor
**Branch:** fix-none-address → main

## Description

The order-summary page 500s for orders created before shipping addresses became mandatory. Guard against the missing relation and show a placeholder.

## Diff

```diff
--- a/orders/services.py
+++ b/orders/services.py
@@ def order_summary(order):
-    address = format_address(order.shipping_address)
+    if order.shipping_address is None:
+        address = "(no shipping address on file)"
+    else:
+        address = format_address(order.shipping_address)
```
