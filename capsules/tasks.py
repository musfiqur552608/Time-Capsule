import logging

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def deliver_capsule(self, capsule_id):
    from .models import Capsule

    try:
        capsule = Capsule.objects.get(id=capsule_id)
        send_mail(
            subject=f"⏳ Your time capsule has unlocked: {capsule.title}",
            message=(
                f"You sealed this on {capsule.created_at:%Y-%m-%d}.\n\n"
                f"{capsule.message}\n\n— Your past self"
            ),
            from_email=None,  # falls back to DEFAULT_FROM_EMAIL
            recipient_list=[capsule.recipient_email],
        )
        capsule.status = Capsule.Status.DELIVERED
        capsule.delivered_at = timezone.now()
        capsule.save(update_fields=["status", "delivered_at"])
        return f"delivered capsule {capsule_id}"
    except Exception as exc:
        logger.exception("Delivery failed for capsule %s", capsule_id)
        raise self.retry(exc=exc)