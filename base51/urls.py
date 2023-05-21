from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_form, name="upload_form"),
    path("upload", views.upload_file, name="upload_file"),
    path("send-sms/", views.send_sms, name="send_sms"),
]
