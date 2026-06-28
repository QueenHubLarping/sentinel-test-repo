"""
Checkout endpoint.

ADR-001: the confirmation email is handed to a background Celery queue, not sent
inline. The endpoint writes the order, enqueues the email, and returns 200 right
away — keeping the ~800ms SMTP call off the checkout critical path (p95 540ms, not
1340ms). Do NOT add a synchronous send_email_smtp(...) call here.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from checkout.tasks import send_order_confirmation_task
from orders.services import create_order


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout(request):
    order = create_order(request.user, request.data["cart"])

    # ADR-001: hand the confirmation email to the background queue. Keeps the
    # blocking SMTP call out of the request path. See checkout/tasks.py.
    send_order_confirmation_task.delay(order.id)

    return Response({"order_id": order.id, "status": "confirmed"}, status=201)
