import logging
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException
from .constants import PayoutStatus
from .models import Payout

logger = logging.getLogger(__name__)

class InvalidStateTransitionError(APIException):
    status_code = 409
    default_detail = 'Invalid status transition.'

class PayoutProcessingError(APIException):
    status_code = 422
    default_detail = 'Failed to process payout.'

class PayoutService:
    @staticmethod
    @transaction.atomic
    def create_payout(data, trigger_processing=True):
        payout = Payout.objects.create(**data)
        logger.info(f'Payout created: {payout.id}')
        if trigger_processing:
            from .tasks import process_payout
            transaction.on_commit(lambda: process_payout.delay(str(payout.id)))
        return payout

    @staticmethod
    @transaction.atomic
    def update_payout(payout, data):
        if payout.is_terminal:
            raise InvalidStateTransitionError(f'Cannot update payout in {payout.status} status.')
        for field, value in data.items():
            setattr(payout, field, value)
        payout.save()
        return payout

    @staticmethod
    @transaction.atomic
    def process_payout(payout_id):
        try:
            payout = Payout.objects.select_for_update().get(id=payout_id)
        except Payout.DoesNotExist:
            raise PayoutProcessingError(f'Payout {payout_id} not found.')

        if payout.status != PayoutStatus.PENDING:
            return payout

        payout.status = PayoutStatus.PROCESSING
        payout.save(update_fields=['status', 'updated_at'])

        try:
            if payout.amount > 1_000_000:
                raise PayoutProcessingError('Amount exceeds limit.')
            if 'TEST_FAIL' in payout.recipient_name.upper():
                raise PayoutProcessingError('Invalid recipient.')

            payout.status = PayoutStatus.COMPLETED
            payout.processed_at = timezone.now()
            payout.save(update_fields=['status', 'processed_at', 'updated_at'])
            logger.info(f'Payout {payout_id} completed')
        except Exception as e:
            payout.status = PayoutStatus.FAILED
            payout.failure_reason = str(e)
            payout.save(update_fields=['status', 'failure_reason', 'updated_at'])
            raise
        return payout

    @staticmethod
    @transaction.atomic
    def cancel_payout(payout_id):
        payout = Payout.objects.select_for_update().get(id=payout_id)
        if not payout.can_be_cancelled:
            raise InvalidStateTransitionError(f'Cannot cancel payout in {payout.status} status.')
        payout.status = PayoutStatus.CANCELLED
        payout.save(update_fields=['status', 'updated_at'])
        return payout
