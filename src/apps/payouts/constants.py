from enum import StrEnum

class PayoutStatus(StrEnum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

    @classmethod
    def choices(cls):
        return [(s.value, s.name.title()) for s in cls]

    @classmethod
    def terminal_statuses(cls):
        return {cls.COMPLETED, cls.FAILED, cls.CANCELLED}

class Currency(StrEnum):
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    RUB = 'RUB'

    @classmethod
    def choices(cls):
        return [(c.value, c.value) for c in cls]
