from django.shortcuts import render
import pandas as pd
from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed

from base51.models import SMSResponse, MessageSender
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

def sms_response(request):
    if request.method == 'POST':
        # Handle the POST request
        # Process the response data and update the database accordingly
        return HttpResponse(status=200)
    elif request.method == 'GET':
        # Handle the GET request
        # Display the response data or perform any necessary actions
        return HttpResponse("GET request received")
    else:
        # Handle other HTTP methods if needed
        return HttpResponse(status=405)


def display_senders(request):
    senders = MessageSender.objects.all()
    context = {'senders': senders}
    return render(request, 'senders.html', context)
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


def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            return render(request, "upload.html", {"error": "No file uploaded"})
        # Read the Excel file using pandas
        try:
            df = pd.read_excel(file)
        except pd.errors.ParserError:
            return render(request, "upload.html", {"error": "Invalid file format. Please upload an Excel file."})

        # Extract the 'PHONE' column
        if 'PHONE' in df.columns:
            cellphones = df['PHONE'].tolist()
            # Render the extracted data in a new template
            context = {"cellphones": cellphones}
            return render(request, "display.html", context)
        else:
            return render(request, "upload.html", {"error": "The uploaded file does not contain the 'PHONE' column."})
    return render(request, "upload.html", {"error": "Invalid request method"})


def upload_form(request):
    return render(request, "upload.html")
