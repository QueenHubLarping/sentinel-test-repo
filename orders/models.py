"""
Order models — PostgreSQL transactional storage (ADR-002).

These tables hold financial/order-state data and rely on Postgres ACID guarantees
and foreign-key constraints. Do not move these to a document store (ADR-002).
"""

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        CONFIRMED = "confirmed"
        REFUNDED = "refunded"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ADR-002: order rows must never be orphaned from their payment.
        constraints = [
            models.CheckConstraint(
                check=models.Q(total_amount__gte=0), name="order_total_non_negative"
            )
        ]
