from django.shortcuts import render
import pandas as pd
from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from twilio.rest import Client


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
        file = request.FILES["file"]
        if not file:
            return render(request, "upload.html", {"error": "No file uploaded"})
        # Read the Excel file using pandas
        df = pd.read_excel(file)
        # Extract the 'name' and 'cellphone' columns
        # names = df['name'].tolist()
        cellphones = df["cellphone"].tolist()
        # Render the extracted data in a new template
        context = {"cellphones": cellphones}
        return render(request, "display.html", context)
    return render(request, "upload.html", {"error": "Invalid request method"})


def upload_form(request):
    return render(request, "upload.html")
