import logging
import random
import time

from celery import shared_task

from .services import PayoutService

logger = logging.getLogger(__name__)


@shared_task(bind=True, name="payouts.process_payout", max_retries=3, acks_late=True)
def process_payout(self, payout_id):
    logger.info(f"Processing payout {payout_id}")
    time.sleep(random.uniform(1, 3))
    try:
        payout = PayoutService.process_payout(payout_id)
        return {"payout_id": str(payout.id), "status": payout.status}
    except Exception as e:
        logger.error(f"Error processing payout {payout_id}: {e}")
        raise self.retry(exc=e) from e
