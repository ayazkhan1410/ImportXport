from django.shortcuts import render, redirect
from automation.models import *
from django.apps import apps
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from uploads.models import Upload
from django.conf import settings
import time
from .tasks import celery_email_send, import_data_task, export_data_task
from .helpers import *
import datetime
from django.core.management import call_command

User = get_user_model()  

def home(request):
    return render(request, 'automation/home.html')

def import_data(request):
    if request.method == "POST":
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name') 
        
        if file_path.size > 10 * 1024 * 1024: 
            messages.error(request, "File size must be under 2 MB.")
            return redirect('import_data')
        
        # Store the file and Model into Upload Model   
        upload_obj = Upload.objects.create(
            file=file_path,
            model_name=model_name
        )
        
        # Construct The Full PATH
        relative_path = str(upload_obj.file.url)
        base_path = str(settings.BASE_DIR)
        file_path = base_path + relative_path  # Absolute path

        # Check for the csv error
        try:
            check_csv_errors(file_path, model_name)
        except Exception as err:
            messages.error(request, str(err))
            return redirect('import_data')
        # Handle the import data task here
        import_data_task.delay(file_path, model_name)
        
        # Show the message to the User
        messages.success(request, "You will be get notified once you're data has been imported")
        return redirect('import_data')

    custom_models = get_all_custom_models()
    context = {
        'custom_models': custom_models
    }
    return render(request, "automation/index.html", context)

def export_data(request):
    if request.method == "POST":
        model_name = request.POST.get('model_name')
        
        # Handle the export data task
        export_data_task.delay(model_name)
        
        # Show the message to the User
        messages.success(request, "You will be get notified once you're data has been Exported")
        return redirect('export_data')

    custom_models = get_all_custom_models()
    context = {
        'custom_models': custom_models
    }
    return render(request, 'automation/export-data.html', context)

# Testing View
def email_send(request):
    celery_email_send.delay()
    return HttpResponse("<h1> Email Testing Function in Django </h1>")

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') 
                
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return render(request, 'automation/login.html')

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)

            if not remember_me:
                request.session.set_expiry(0) 
            else:
                request.session.set_expiry(1209600)  # 2 weeks
                
            return redirect('index')
        else:
            print("Invalid email or password")
            messages.error(request, "Invalid email or password")

    return render(request, 'automation/login.html')

def signup(request):
    return render(request, 'automation/signup.html')