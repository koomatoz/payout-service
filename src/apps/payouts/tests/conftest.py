import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def payout_data():
    return {
        "amount": "100.50",
        "currency": "USD",
        "recipient_name": "John Doe",
        "recipient_account": "DE89370400440532013000",
        "recipient_bank_code": "COBADEFFXXX",
        "description": "Test payout",
    }
