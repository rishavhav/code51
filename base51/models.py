from django.db import models

class SMSResponse(models.Model):
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.timestamp}"

class MessageSender(models.Model):
    phone_number = models.CharField(max_length=20)
    sms_response = models.ForeignKey(SMSResponse, on_delete=models.SET_NULL, null=True, blank=True)
    date_received = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number
