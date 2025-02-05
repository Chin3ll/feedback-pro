# Generated by Django 5.1.3 on 2025-02-05 18:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationCriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_syntax', models.BooleanField(default=True, help_text='Check for syntactic accuracy.')),
                ('check_indentation', models.BooleanField(default=True, help_text='Check for correct indentation.')),
                ('check_comments', models.BooleanField(default=True, help_text='Check for good comments.')),
                ('min_comments', models.PositiveIntegerField(default=1, help_text='Minimum required comments in the code.')),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the evaluation or assignment.', max_length=255)),
                ('student_code', models.TextField(help_text="The student's submitted code.")),
                ('feedback', models.TextField(help_text="Detailed feedback for the student's submission.")),
                ('tutor_feedback', models.TextField(blank=True, help_text='Tutor specific feedback for the submission.', null=True)),
                ('correctness', models.BooleanField(default=False, help_text='Indicates whether the submission is correct.')),
                ('time_complexity', models.CharField(default='Unknown', help_text='Time complexity of the submitted solution.', max_length=50)),
                ('grade', models.FloatField(blank=True, help_text='Grade awarded for the evaluation (out of 100).', null=True)),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('reviewed', 'Reviewed'), ('pending', 'Pending Review')], default='pending', help_text='Current status of the evaluation.', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the evaluation was created.')),
                ('student', models.ForeignKey(help_text='The student who submitted the evaluation.', on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100)),
                ('algorithm', models.CharField(max_length=50)),
                ('code', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
