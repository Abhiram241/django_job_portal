# Generated by Django 5.0.6 on 2024-07-07 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_user_details_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='linkedin_page',
            field=models.CharField(default='https://www.youtube.com/', max_length=100),
        ),
    ]
