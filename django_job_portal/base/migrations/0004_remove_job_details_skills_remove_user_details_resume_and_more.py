# Generated by Django 5.0.6 on 2024-07-03 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_job_details_job_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_details',
            name='skills',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='resume',
        ),
        migrations.AddField(
            model_name='user_details',
            name='skills',
            field=models.TextField(blank=True, null=True),
        ),
    ]
