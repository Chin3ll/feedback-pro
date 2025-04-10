# Generated by Django 5.1.3 on 2025-02-08 18:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorting_feedback', '0004_evaluation_submission_file_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='is_plagiarized',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='plagiarism_score',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='required_construct',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='tutor_feedback',
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='correctness',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='feedback',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='grade',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='status',
            field=models.CharField(choices=[('submitted', 'Submitted'), ('reviewed', 'Reviewed')], default='submitted', max_length=50),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='student_code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='submission_file',
            field=models.FileField(blank=True, null=True, upload_to='submissions/'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='time_complexity',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
