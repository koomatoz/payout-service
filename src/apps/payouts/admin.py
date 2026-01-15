from django.contrib import admin

from .models import Payout


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ["id", "amount", "currency", "recipient_name", "status", "created_at"]
    list_filter = ["status", "currency"]
    readonly_fields = ["id", "created_at", "updated_at", "processed_at"]
