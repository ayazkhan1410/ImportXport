from django.shortcuts import render, redirect
from automation.models import *
from django.apps import apps
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.core.management import call_command, CommandError

User = get_user_model()  

def get_all_custom_models():
    default_models = ["Group", "Permission", "Session", "ContentType","LogEntry","User","Upload"]
    custom_models = []

    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if model.__name__ not in default_models:
                custom_models.append(model.__name__)
    return custom_models


def index(request):
    if request.method == "POST":
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name') 
        
        if file_path.size > 10 * 1024 * 1024: 
            messages.error(request, "File size must be under 2 MB.")
            return redirect('/')
        
        # Store the file and Model into Upload Model   
        upload_obj = Upload.objects.create(
            file=file_path,
            model_name=model_name
        )
        
        # Construct The Full PATH
        relative_path = str(upload_obj.file.url)
        base_path = str(settings.BASE_DIR)
        file_path = base_path + relative_path  # Absolute path

        # Trigger The Command
        try:
            call_command('importdata', file_path, model_name)
            messages.success(request, "Data successfully inserted into the table.")
        except CommandError as ce:  
            messages.error(request, f"Error: {str(ce)}")
        except Exception as e:  
            messages.error(request, f"{str(e)}")

        return redirect('/')

    custom_models = get_all_custom_models()
    context = {
        'custom_models': custom_models
    }
    return render(request, "automation/index.html", context)

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