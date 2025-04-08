# Generated by Django 5.1.5 on 2025-04-08 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttendeeUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(default='default@example.com', max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('pfp', models.ImageField(upload_to='profile_pics/')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizerUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(default='default@example.com', max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('pfp', models.ImageField(upload_to='profile_pics/')),
            ],
        ),
    ]
