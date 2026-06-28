"""
Order creation service.

Order + payment rows are written inside a single atomic transaction (ADR-002):
Postgres guarantees an order can never be persisted without its matching payment.
"""

from decimal import Decimal

from django.db import transaction

from orders.models import Order
from payments.models import Payment


@transaction.atomic
def create_order(user, cart) -> Order:
    """Create an order and its payment atomically (ADR-002)."""
    total = sum((Decimal(str(item["price"])) * item["qty"] for item in cart), Decimal("0"))

    order = Order.objects.create(user=user, total_amount=total, status=Order.Status.CONFIRMED)
    Payment.objects.create(order=order, amount=total, status=Payment.Status.CAPTURED)
    return order
