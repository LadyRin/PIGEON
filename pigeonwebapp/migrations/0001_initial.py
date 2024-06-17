# Generated by Django 5.0.6 on 2024-06-17 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('speaker_first_name', models.CharField(max_length=100)),
                ('speaker_last_name', models.CharField(max_length=100)),
                ('speaker_from', models.CharField(max_length=100)),
                ('speaker_comment', models.TextField()),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('description', models.TextField()),
                ('attachment', models.FileField(upload_to='attachments/')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigeonwebapp.eventtheme')),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigeonwebapp.eventtype')),
                ('mailing_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigeonwebapp.mailinglist')),
            ],
        ),
    ]