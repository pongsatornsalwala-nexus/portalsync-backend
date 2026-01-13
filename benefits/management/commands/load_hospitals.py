# For reading JSON files
import json
# Base class for commands
from django.core.management.base import BaseCommand
# The hospital model
from benefits.models import Hospital

# Django looks for a class named `Command` in the file
# `help` text shows when running `python` manage.py help load_hospitals
class Command(BaseCommand):
    help = 'Load hospital data from JSON file into the database'

    # Main function
    def handle(self, *args, **kwargs):
        # Path to the JSON file
        json_file_path = '/Users/Bamee/Desktop/portalsync-backend/Complete SSO Hospital List for Django.json'

        # Open and read the JSON file
        self.stdout.write('Loading hospital data ...')

        # Read JSON file
        # Opens the file
        # `encoding = 'utf-8'` handles Thai characters properly
        # `json.load()` converts JSON to Python list
        with open(json_file_path, 'r', encoding = 'utf-8') as file:
            hospitals_data = json.load(file)

        # Counter for tracking
        created_count = 0
        
        # Loop through each hospital in the JSON
        for hospital_data in hospitals_data:
            # Create or update hospital
            # Check if hospital exists by name and province
            # Returns a tuple: `(hospital_object, True/False)`
            hospital, created = Hospital.objects.get_or_create(
                name = hospital_data['name'],
                province = hospital_data['province'],
                defaults = {
                    'hospital_type': hospital_data['type']
                }
            )

            if created:
                created_count += 1

        # Success message
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {created_count} hospitals!'
            )
        )