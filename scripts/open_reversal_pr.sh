#!/usr/bin/env bash
#
# Open a pull request that REVERSES ADR-001 (async email) — it makes the checkout
# confirmation email synchronous again. Sentinel should flag it.
#
# Uses the GitHub REST API directly (no gh CLI needed). Requires a Personal Access
# Token with `repo` scope:
#
#   GITHUB_TOKEN=<your-pat> ./scripts/open_reversal_pr.sh
#
set -euo pipefail

REPO="Notchayan/sentinel-test-repo"
BASE="main"
HEAD="reverse-async-email"
: "${GITHUB_TOKEN:?Set GITHUB_TOKEN to a PAT with 'repo' scope}"

# 1. Create the reversing branch locally from main (if it doesn't exist yet).
if ! git rev-parse --verify "$HEAD" >/dev/null 2>&1; then
  git checkout -b "$HEAD" "$BASE"

  # --- Reverse ADR-001: send the confirmation email inline, drop the Celery task. ---
  cat > checkout/views.py <<'PY'
"""
Checkout endpoint.

Simplified: send the confirmation email directly instead of via the queue. One
fewer moving part to deploy.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from email_service.smtp import render_confirmation, send_email_smtp
from orders.services import create_order


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout(request):
    order = create_order(request.user, request.data["cart"])

    # Send the confirmation email directly — simpler, no queue needed.
    send_email_smtp(order.user.email, render_confirmation(order))

    return Response({"order_id": order.id, "status": "confirmed"}, status=201)
PY

  git rm -q checkout/tasks.py
  git commit -aqm "Simplify checkout: send confirmation email synchronously"
  git checkout -q "$BASE"
fi

# 2. Push the branch.
git push -u origin "$HEAD"

# 3. Open the PR via the GitHub API.
curl -sS -X POST \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/${REPO}/pulls" \
  -d @- <<JSON
{
  "title": "Simplify checkout: send confirmation email synchronously",
  "head": "${HEAD}",
  "base": "${BASE}",
  "body": "The Celery + Redis setup for confirmation emails feels like overkill and adds a service to deploy. This sends the email inline via SendGrid SMTP before returning. One fewer service to run."
}
JSON

echo
echo "PR opened. Sentinel should run on it and flag the ADR-001 reversal."
