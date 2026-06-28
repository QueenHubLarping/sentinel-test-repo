"""
Background email dispatch (ADR-001).

The confirmation email is sent here, on a Celery worker, OUTSIDE the checkout
request/response cycle. This is what keeps the ~800ms SendGrid SMTP call off the
checkout critical path. Retries use exponential backoff (3 attempts, max 1 min).
"""

from smtplib import SMTPException

from celery import shared_task

from email_service.smtp import render_confirmation, send_email_smtp
from orders.models import Order


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation_task(self, order_id: int) -> None:
    """Dispatch the order-confirmation email asynchronously.

    Invoked via `.delay(order_id)` from the checkout view so the HTTP worker
    returns immediately. Never call send_email_smtp inline in the view (ADR-001).
    """
    order = Order.objects.get(id=order_id)
    try:
        send_email_smtp(order.user.email, render_confirmation(order))
    except SMTPException as exc:
        # Exponential backoff retry — transactional email reliability (ADR-001).
        raise self.retry(exc=exc, countdown=min(60, 2 ** self.request.retries))
