# Generated by Django 5.0.6 on 2024-07-08 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0005_remove_appointment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('D', 'Declined')], default='P', max_length=1),
        ),
    ]
