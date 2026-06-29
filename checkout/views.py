"""
Checkout endpoint.

Sends the confirmation email inline — simpler, one fewer service to run.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from email_service.smtp import send_email_smtp
from orders.services import create_order


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout(request):
    order = create_order(request.user, request.data["cart"])

    # Send the confirmation email directly — no background queue needed.
    send_email_smtp(order.user.email, f"Order {order.id} confirmed")

    return Response({"order_id": order.id, "status": "confirmed"}, status=201)
