import factory
from factory.django import DjangoModelFactory

from apps.payouts.constants import Currency, PayoutStatus
from apps.payouts.models import Payout


class PayoutFactory(DjangoModelFactory):
    class Meta:
        model = Payout

    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    currency = Currency.USD
    recipient_name = factory.Faker("name")
    recipient_account = "DE89370400440532013000"
    recipient_bank_code = "COBADEFFXXX"
    status = PayoutStatus.PENDING
    description = factory.Faker("sentence")
