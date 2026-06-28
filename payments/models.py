"""
Payment models — PostgreSQL transactional storage (ADR-002).

A payment is bound to exactly one order by a foreign key. ACID guarantees keep
order and payment writes atomic; refunds cannot partially apply.
"""

from django.db import models

from orders.models import Order


class Payment(models.Model):
    class Status(models.TextChoices):
        CAPTURED = "captured"
        REFUNDED = "refunded"
        FAILED = "failed"

    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)
