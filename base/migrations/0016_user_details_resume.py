# Generated by Django 5.0.6 on 2024-07-07 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_user_details_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
    ]