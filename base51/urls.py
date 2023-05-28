from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_form, name="upload_form"),
    path("upload/", views.upload_file, name="upload_file"),
    path("send-sms/", views.send_sms, name="send_sms"),
    path('sms-response/', views.sms_response, name='sms_response'),
    path('senders/', views.display_senders, name='display_senders'),
    path('delete_senders/', views.delete_senders, name='delete_senders'),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
]
