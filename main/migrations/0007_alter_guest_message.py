# Generated by Django 5.0.4 on 2024-05-04 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_number_of_guests_guest_number_of_guests_attending_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
