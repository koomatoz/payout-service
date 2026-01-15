from decimal import Decimal

from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from core.models import TimeStampedModel, UUIDModel

from .constants import Currency, PayoutStatus


class Payout(UUIDModel, TimeStampedModel):
    amount = models.DecimalField(
        max_digits=18, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    currency = models.CharField(max_length=3, choices=Currency.choices(), default=Currency.USD)
    recipient_name = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    recipient_account = models.CharField(max_length=34, validators=[MinLengthValidator(8)])
    recipient_bank_code = models.CharField(max_length=11, blank=True, default="")
    status = models.CharField(
        max_length=20, choices=PayoutStatus.choices(), default=PayoutStatus.PENDING, db_index=True
    )
    description = models.TextField(blank=True, default="", max_length=1000)
    processed_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True, default="")

    class Meta:
        db_table = "payouts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payout {self.id} - {self.amount} {self.currency}"

    @property
    def is_terminal(self):
        return PayoutStatus(self.status) in PayoutStatus.terminal_statuses()

    @property
    def can_be_cancelled(self):
        return self.status == PayoutStatus.PENDING
