# PR #83: Persist user sessions in the database for instant revocation

**Author:** @new-contributor
**Branch:** db-backed-sessions → main

## Description

Support keeps asking for a "log this user out everywhere" button. The cleanest way is classic server-side sessions: keep a row per session so an admin can delete it and the user is out immediately. This PR switches auth back to Django's DB session backend and looks the session up on each request — standard, boring, battle-tested.

## Diff

```diff
--- a/config/settings.py
+++ b/config/settings.py
@@
+SESSION_ENGINE = "django.contrib.sessions.backends.db"
+MIDDLEWARE.insert(0, "django.contrib.sessions.middleware.SessionMiddleware")

--- a/auth/middleware.py
+++ b/auth/middleware.py
@@ def authenticate(request):
-    claims = verify_token_signature(request.headers["Authorization"])
-    request.user = User.from_claims(claims)
+    # look the session up so admins can revoke it row-by-row
+    session = Session.objects.get(session_key=request.COOKIES["sessionid"])
+    request.user = session.user
```
