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
