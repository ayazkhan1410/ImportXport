from django.apps import apps
from django.core.management.base import BaseCommand,CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings

def get_all_custom_models():
    default_models = ["Group", "Permission", "Session", "ContentType","LogEntry","User","Upload"]
    custom_models = []

    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if model.__name__ not in default_models:
                custom_models.append(model.__name__)
    return custom_models

def check_csv_errors(file_path,model_name):
    model = None
    
    # Search for the model across all the app
    for item in apps.get_app_configs():
        try:
            model = apps.get_model(item.label, model_name)
            break # stop searching if model found
        except LookupError:
            continue # Continue for searching app
    
    if not model:
        raise CommandError(f"Model {model_name} not Found in any app")
    
    # Compare CSV headers with model field names
    # get model fields
    model_field = [field.name for field in model._meta.fields if field.name != 'id']
    
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            
            # Compare both model fields and CSV header
            if model_field != csv_header:
                raise DataError(f"CSV File doesn't match with {model_name} table fields")
    except Exception as e:
        raise e
    
    return model

def send_email_notification(mail_subject, message, to_email):
    try:
        from_email = settings.EMAIL_HOST_USER
        mail = EmailMessage(mail_subject, message, from_email, to_email)
        mail.send()
    except Exception as e:
        raise e