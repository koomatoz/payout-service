from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .constants import PayoutStatus
from .models import Payout
from .serializers import PayoutCreateSerializer, PayoutSerializer
from .services import PayoutService


class PayoutFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=PayoutStatus.choices())
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Payout
        fields = ["status", "currency"]


@extend_schema_view(
    list=extend_schema(summary="List payouts", tags=["Payouts"]),
    retrieve=extend_schema(summary="Get payout", tags=["Payouts"]),
    create=extend_schema(summary="Create payout", tags=["Payouts"]),
    partial_update=extend_schema(summary="Update payout", tags=["Payouts"]),
    destroy=extend_schema(summary="Delete payout", tags=["Payouts"]),
)
class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.all()
    filterset_class = PayoutFilter
    serializer_class = PayoutSerializer
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return PayoutCreateSerializer
        return PayoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payout = PayoutService.create_payout(serializer.validated_data)
        return Response(PayoutSerializer(payout).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        payout = self.get_object()
        serializer = self.get_serializer(payout, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = PayoutService.update_payout(payout, serializer.validated_data)
        return Response(PayoutSerializer(updated).data)

    def destroy(self, request, *args, **kwargs):
        payout = self.get_object()
        if payout.status != PayoutStatus.PENDING:
            return Response(
                {"detail": "Only pending payouts can be deleted."}, status=status.HTTP_409_CONFLICT
            )
        payout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(summary="Cancel payout", tags=["Payouts"])
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        payout = PayoutService.cancel_payout(pk)
        return Response(PayoutSerializer(payout).data)
