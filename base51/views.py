from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from base51.models import SMSResponse, MessageSender
import pandas as pd
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import render
from twilio.rest import Client
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.http import JsonResponse


def send_message(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        message = request.POST.get("message")

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )

        return JsonResponse({"success": True})

    return render(request, "send_message.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("upload_file")
        else:
            # Invalid credentials, show an error message
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


@login_required(login_url="login")
def delete_messages(request):
    if request.method == "POST":
        selected_messages = request.POST.getlist("selected_messages")

        # Delete the selected messages from the database
        SMSResponse.objects.filter(id__in=selected_messages).delete()

    return redirect("display_senders")


@login_required(login_url="login")
def delete_senders(request):
    if request.method == "POST":
        sender_ids = request.POST.getlist("sender_ids")
        # Logic for deleting senders from the database using the sender_ids list
        # ...

        messages.success(request, "Senders deleted successfully.")
    return redirect("display_senders")


def distinct_total_numbers(total_messages):
    senders_dict = {}
    for response in total_messages:
        phone_number = response.phone_number
        message = response.message

        if phone_number in senders_dict:
            senders_dict[phone_number].append(message)
        else:
            senders_dict[phone_number] = [message]

    senders = []
    for phone_number, messages in senders_dict.items():
        sender = {"phone_number": phone_number, "messages": messages}
        senders.append(sender)
    return len(senders)


@login_required(login_url="login")
def display_senders(request):
    total_messages = distinct_total_numbers(SMSResponse.objects.all())
    sms_responses = SMSResponse.objects.filter(seen=False)

    senders_dict = {}

    for response in sms_responses:
        phone_number = response.phone_number
        message = response.message

        if phone_number in senders_dict:
            senders_dict[phone_number].append(message)
        else:
            senders_dict[phone_number] = [message]

    senders = []
    for phone_number, messages in senders_dict.items():
        sender = {"phone_number": phone_number, "messages": messages}
        senders.append(sender)

    context = {
        "senders": senders,
        "message_counter": len(senders),
        "total_messages": total_messages,
    }
    return render(request, "senders.html", context)


@login_required(login_url="login")
def mark_as_seen(request):
    if request.method == "POST":
        sender_phone_numbers = request.POST.getlist("sender_ids")
        sender_phone_numbers = [
            phone_number for phone_number in sender_phone_numbers if phone_number
        ]

        SMSResponse.objects.filter(phone_number__in=sender_phone_numbers).update(
            seen=True, timestamp=timezone.now()
        )

    return redirect("display_senders")


@login_required(login_url="login")
def send_sms(request):
    if request.method == "POST":
        phone_numbers = request.POST.getlist("phone_numbers[]")
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        success_count = 0

        for phone_number in phone_numbers:
            try:
                message = client.messages.create(
                    body="hey I am Rishav Soam. wanted to tell you that I am looking for you!",
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=phone_number,
                )
                success_count += 1
            except Exception as e:
                # Handle any exceptions that occur during message sending
                messages.error(
                    request, f"Error sending SMS to {phone_number}: {str(e)}"
                )

        if success_count > 0:
            messages.success(
                request,
                f"SMS messages sent successfully to {success_count} recipient(s).",
            )
        else:
            messages.warning(request, "Failed to send SMS messages.")

        return redirect("upload_file")

    senders = MessageSender.objects.filter(seen=False)
    context = {"senders": senders}
    return render(request, "display.html", context)


@login_required(login_url="login")
def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            return render(request, "upload.html", {"error": "No file uploaded"})
        df = pd.read_excel(file)

        phone_numbers = df["PHONE"].tolist()
        return render(request, "display.html", {"phone_numbers": phone_numbers})

    return render(request, "upload.html", {"error": "Invalid request method"})


@login_required(login_url="login")
def upload_form(request):
    return render(request, "upload.html")


@csrf_exempt
def sms_response(request):
    if request.method == "POST":
        phone_number = request.POST.get("From")
        message = request.POST.get("Body")
        response = SMSResponse(phone_number=phone_number, message=message)
        response.save()
        sender, created = MessageSender.objects.get_or_create(phone_number=phone_number)
        sender.sms_response = response
        sender.save()

        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed(["POST"])
