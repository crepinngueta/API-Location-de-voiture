# Generated by Django 4.2.7 on 2024-07-30 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_remove_contact_first_name_remove_contact_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]