from django.core.management.base import BaseCommand,CommandError
import csv
from django.apps import apps

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
                
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                
                for data in reader:
                    if model.objects.filter(roll_number = data['roll_number']).exists():
                        self.stderr.write(self.style.ERROR(f"student with this {data['roll_number']} already exists"))
                    else:
                        model.objects.create(**data) 
                        self.stdout.write(self.style.SUCCESS("Data inserted successfully"))   
            self.stdout.write(self.style.SUCCESS("Query Run successfully.."))
        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except Exception as e:
            print(e)