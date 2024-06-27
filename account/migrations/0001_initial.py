# Generated by Django 4.2.7 on 2024-06-26 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('name', models.CharField(max_length=200)),
                ('tc', models.BooleanField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.BooleanField(default=False)),
                ('owner', models.BooleanField(default=False)),
                ('id_card_number', models.CharField(default='default_value', max_length=50, unique=True)),
                ('driving_license_photo', models.ImageField(blank=True, null=True, upload_to='licenses/')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]