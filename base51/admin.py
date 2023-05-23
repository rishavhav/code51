from django.contrib import admin
from .models import SMSResponse, MessageSender

@admin.register(SMSResponse)
class SMSResponseAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'message', 'timestamp')

@admin.register(MessageSender)
class MessageSenderAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'date_received')