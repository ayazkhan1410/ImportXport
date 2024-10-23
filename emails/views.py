from django.shortcuts import render, redirect
from .forms import EmailForm
from .models import *
from django.contrib import messages
from automation.helpers import send_email_notification_bulk
from django.conf import settings
from .tasks import celery_bulk_email_send

def send_email(request):
    if request.method == "POST":
        email_list_id = request.POST.get('email_list')
        body = request.POST.get('body')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')  

        try:
            email_list = List.objects.get(id=email_list_id)   
            
            email_obj = Email.objects.create(
                email_list=email_list,
                body=body,
                message=message,
                attachment=attachment if attachment else None
            )

            # Recipients List
            to_email = []
            try:
                sample = Subscriber.objects.filter(email_list = email_list)
                to_email = [item.email_address for item in sample]
            except Exception as e:
                messages.error(request, str(e))

            # Send Email
            if not to_email:
                messages.error(request, "No recipients found in the selected email list. Please ensure that the email list has subscribers.")
            else:
                # Handover task to celery
                celery_bulk_email_send.delay(body, message, to_email, attachment)
                messages.success(request, "Email sent successfully!")
            return redirect('send_email')
        except List.DoesNotExist:
            messages.error(request, "Invalid email list selected.")
    else:       
        email_list = List.objects.only("email_list")
        context = {
            'email_list': email_list
        }
        return render(request, 'emails/send_email.html', context)