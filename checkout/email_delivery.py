# checkout/email_delivery.py
# Reversal demo: send the order-confirmation email synchronously, inline in checkout.
from email_service.smtp import send_email_smtp

def deliver_confirmation(order):
    # was: send_order_confirmation.delay(order.id)  (async via Celery/Redis)
    send_email_smtp(order.user.email, render_confirmation(order))
