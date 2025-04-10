# Generated by Django 5.1.3 on 2025-02-14 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorting_feedback', '0012_evaluationcriteria_allowed_loop_types_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationcriteria',
            name='max_loop_iterations',
            field=models.JSONField(blank=True, default=dict, help_text="Set max allowed iterations per loop type, e.g., {'for': 3, 'while': 2}.", null=True),
        ),
    ]
