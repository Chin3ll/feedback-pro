# Generated by Django 5.1.3 on 2025-02-08 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorting_feedback', '0002_evaluationcriteria_required_constructs'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='is_plagiarized',
            field=models.BooleanField(default=False, help_text='Indicates if plagiarism is detected.'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='plagiarism_score',
            field=models.FloatField(default=0.0, help_text='Plagiarism percentage score.'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='required_construct',
            field=models.CharField(blank=True, help_text="The mandatory construct required in the submission (e.g., 'while loop', 'function').", max_length=50, null=True),
        ),
    ]
