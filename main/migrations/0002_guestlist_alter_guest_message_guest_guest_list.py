# Generated by Django 5.0.4 on 2024-05-03 20:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the guest list or event.', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Description of the guest list or event.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='guest',
            name='message',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='guest_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guests', to='main.guestlist'),
        ),
    ]
