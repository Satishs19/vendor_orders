# Generated by Django 5.2.4 on 2025-07-19 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='vendor_name',
        ),
    ]
