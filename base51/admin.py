from django.contrib import admin
from .models import SMSResponse


@admin.register(SMSResponse)
class SMSResponseAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "message", "timestamp", "seen")
    list_filter = ("seen",)
    search_fields = ("phone_number", "message")
