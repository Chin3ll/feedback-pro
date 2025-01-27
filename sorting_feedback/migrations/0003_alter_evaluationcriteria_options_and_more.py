# Generated by Django 5.1.3 on 2025-01-26 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorting_feedback', '0002_evaluationcriteria'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evaluationcriteria',
            options={},
        ),
        migrations.RemoveField(
            model_name='evaluationcriteria',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='evaluationcriteria',
            name='name',
        ),
        migrations.AddField(
            model_name='evaluationcriteria',
            name='check_comments',
            field=models.BooleanField(default=True, help_text='Check for good comments.'),
        ),
        migrations.AddField(
            model_name='evaluationcriteria',
            name='check_indentation',
            field=models.BooleanField(default=True, help_text='Check for correct indentation.'),
        ),
        migrations.AddField(
            model_name='evaluationcriteria',
            name='check_syntax',
            field=models.BooleanField(default=True, help_text='Check for syntactic accuracy.'),
        ),
        migrations.AddField(
            model_name='evaluationcriteria',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='evaluationcriteria',
            name='min_comments',
            field=models.PositiveIntegerField(default=1, help_text='Minimum required comments in the code.'),
        ),
    ]
