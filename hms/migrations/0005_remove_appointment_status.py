# Generated by Django 5.0.6 on 2024-07-08 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0004_appointment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='status',
        ),
    ]
