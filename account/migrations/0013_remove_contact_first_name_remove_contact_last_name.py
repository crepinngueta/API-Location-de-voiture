# Generated by Django 4.2.7 on 2024-07-30 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_contact_client_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='last_name',
        ),
    ]
