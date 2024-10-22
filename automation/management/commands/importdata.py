from django.core.management.base import BaseCommand,CommandError
import csv
from django.apps import apps
from django.db import DataError

# Proposed Command --> python manage.py importdata filepath + model name
class Command(BaseCommand):
    help = "This command will import data from csv File"
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Importing Data")
        parser.add_argument('model_name', type=str, help="Takes Model Name")
    
    def handle(self, *args, **kwargs):
        try:
            file_path = kwargs['file_path']
            model_name = kwargs['model_name'].capitalize()
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
            
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                csv_header = reader.fieldnames
                
                # Compare both model fields and CSV header
                if model_field != csv_header:
                    raise DataError(f"CSV File doesn't match with {model_name} table fields")
                
                for data in reader:
                    model.objects.create(**data)
                    
                self.stdout.write(self.style.SUCCESS("Data inserted successfully"))   
        except FileNotFoundError:
            raise CommandError(f"File {file_path} not found.")
        except csv.Error as e:
            raise CommandError(f"CSV error: {str(e)}")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")