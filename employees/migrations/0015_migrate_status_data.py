from django.db import migrations

def migrate_status_forward(apps, schema_editor):
    Employee = apps.get_model('employees', 'Employee')

    # Map old values to new values
    status_map = {
        'ENTRY': 'IMPORTED',
        'REVIEWING': 'PENDING',
        'REPORTED': 'PENDING',
        'VERIFIED': 'REGISTERED',
        # PENDING stays PENDING, no mapping needed
    }

    for old_value, new_value in status_map.items():
        Employee.objects.filter(status=old_value).update(status=new_value)
        Employee.objects.filter(ssf_status=old_value).update(ssf_status=new_value)
        Employee.objects.filter(aia_status=old_value).update(aia_status=new_value)

class Migration(migrations.Migration):
    dependencies = [
        ('employees', '0014_simplify_status_to_3_stages'),
    ]
    operations = [
        migrations.RunPython(migrate_status_forward),
    ]