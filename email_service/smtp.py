"""
Low-level email delivery via SendGrid SMTP.

NOTE (ADR-001): `send_email_smtp` performs a *blocking* network call to SendGrid
that was measured at ~800ms p95. It must only ever be invoked from the background
Celery worker (see checkout/tasks.py) — never inline inside a request handler.
Calling it directly from a view reintroduces the latency ADR-001 removed.
"""

import smtplib
from email.mime.text import MIMEText

SENDGRID_SMTP_HOST = "smtp.sendgrid.net"
SENDGRID_SMTP_PORT = 587


def render_confirmation(order) -> str:
    """Render the order-confirmation email body for an Order."""
    lines = [
        f"Hi {order.user.name},",
        "",
        f"Thanks for your order #{order.id}. We've received your payment of "
        f"${order.total_amount:.2f} and your items are on the way.",
        "",
        "— The Shop",
    ]
    return "\n".join(lines)


def send_email_smtp(to_email: str, body: str, subject: str = "Your order confirmation") -> None:
    """Send an email synchronously over SendGrid SMTP.

    This blocks for ~800ms. Do not call from the request path (ADR-001).
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "orders@example.com"
    msg["To"] = to_email

    with smtplib.SMTP(SENDGRID_SMTP_HOST, SENDGRID_SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login("apikey", _sendgrid_api_key())
        smtp.send_message(msg)


def _sendgrid_api_key() -> str:
    import os

    return os.environ["SENDGRID_API_KEY"]
