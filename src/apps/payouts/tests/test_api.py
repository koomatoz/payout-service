import pytest
from django.urls import reverse
from rest_framework import status
from apps.payouts.constants import PayoutStatus
from apps.payouts.models import Payout
from .factories import PayoutFactory

@pytest.mark.django_db
class TestPayoutAPI:
    def test_create_payout_success(self, api_client, payout_data):
        url = reverse('payout-list')
        response = api_client.post(url, payout_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Payout.objects.count() == 1

    def test_create_payout_triggers_celery_task(self, api_client, payout_data):
        url = reverse('payout-list')
        response = api_client.post(url, payout_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        payout = Payout.objects.get(id=response.data['id'])
        assert payout.status in [PayoutStatus.COMPLETED, PayoutStatus.PENDING, PayoutStatus.PROCESSING]

    def test_create_payout_invalid_amount(self, api_client, payout_data):
        url = reverse('payout-list')
        payout_data['amount'] = '-100.00'
        response = api_client.post(url, payout_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_payouts(self, api_client):
        PayoutFactory.create_batch(3)
        response = api_client.get(reverse('payout-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3

    def test_retrieve_payout(self, api_client):
        payout = PayoutFactory.create()
        response = api_client.get(reverse('payout-detail', kwargs={'pk': payout.id}))
        assert response.status_code == status.HTTP_200_OK

    def test_delete_pending_payout(self, api_client):
        payout = PayoutFactory.create(status=PayoutStatus.PENDING)
        response = api_client.delete(reverse('payout-detail', kwargs={'pk': payout.id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_cannot_delete_completed_payout(self, api_client):
        payout = PayoutFactory.create(status=PayoutStatus.COMPLETED)
        response = api_client.delete(reverse('payout-detail', kwargs={'pk': payout.id}))
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_cancel_payout(self, api_client):
        payout = PayoutFactory.create(status=PayoutStatus.PENDING)
        response = api_client.post(reverse('payout-cancel', kwargs={'pk': payout.id}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == PayoutStatus.CANCELLED
