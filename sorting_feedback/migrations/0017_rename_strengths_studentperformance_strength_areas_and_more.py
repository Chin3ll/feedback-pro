# Generated by Django 5.1.3 on 2025-02-15 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sorting_feedback', '0016_studentperformance_last_updated_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentperformance',
            old_name='strengths',
            new_name='strength_areas',
        ),
        migrations.RenameField(
            model_name='studentperformance',
            old_name='weaknesses',
            new_name='weakness_areas',
        ),
    ]
