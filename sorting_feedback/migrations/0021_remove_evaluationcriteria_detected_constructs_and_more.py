# Generated by Django 5.1.3 on 2025-02-16 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sorting_feedback', '0020_evaluationcriteria_detected_constructs_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationcriteria',
            name='detected_constructs',
        ),
        migrations.RemoveField(
            model_name='evaluationcriteria',
            name='missing_constructs',
        ),
    ]
