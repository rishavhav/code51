from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from base51.models import SMSResponse, MessageSender
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
import pandas as pd
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('login')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_file')
        else:
            # Invalid credentials, show an error message
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

@login_required(login_url='login')
def delete_messages(request):
    if request.method == 'POST':
        selected_messages = request.POST.getlist('selected_messages')

        # Delete the selected messages from the database
        SMSResponse.objects.filter(id__in=selected_messages).delete()

    return redirect('display_senders')

@login_required(login_url='login')
def delete_senders(request):
    if request.method == 'POST':
        sender_ids = request.POST.getlist('sender_ids')
        # Logic for deleting senders from the database using the sender_ids list
        # ...

        messages.success(request, 'Senders deleted successfully.')
    return redirect('display_senders')

@login_required(login_url='login')
def display_senders(request):
    # Get the current count from the session, or set it to 0 if it doesn't exist
    count = request.session.get('message_counter', 0)

    senders = SMSResponse.objects.all()
    context = {'senders': senders, 'message_counter': count}
    return render(request, 'senders.html', context)

@login_required(login_url='login')
def send_sms(request):
    if request.method == "POST":
        phone_numbers = request.POST.getlist("phone_numbers[]")

        # Initialize the Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        for phone_number in phone_numbers:
            # Send SMS using Twilio
            message = client.messages.create(
                body="hey I am Rishav Soam. wanted to tell you that i am looking for you!",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number,
            )

        return render(request, "success.html")

    return render(request, "display_numbers.html")

@login_required(login_url='login')
def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            return render(request, "upload.html", {"error": "No file uploaded"})

        # Read the uploaded file using pandas
        df = pd.read_excel(file)

        # Extract the 'PHONE' column values
        phone_numbers = df['PHONE'].tolist()

        # Save the phone numbers to the database or any other processing

        return render(request, "display.html", {"phone_numbers": phone_numbers})

    return render(request, "upload.html", {"error": "Invalid request method"})

@login_required(login_url='login')
def upload_form(request):
    return render(request, "upload.html")

@login_required(login_url='login')
@csrf_exempt
def sms_response(request):
    if request.method == 'POST':
        phone_number = request.POST.get('From')
        message = request.POST.get('Body')

        # Create and save the SMSResponse object
        response = SMSResponse(phone_number=phone_number, message=message)
        response.save()

        # Create or update the MessageSender object
        sender, created = MessageSender.objects.get_or_create(phone_number=phone_number)
        sender.sms_response = response  # Associate the SMSResponse with the MessageSender
        sender.save()

        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed(['POST'])