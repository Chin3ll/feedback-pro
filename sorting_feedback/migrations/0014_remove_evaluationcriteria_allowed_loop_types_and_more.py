# Generated by Django 5.1.3 on 2025-02-14 22:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorting_feedback', '0013_alter_evaluationcriteria_max_loop_iterations'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationcriteria',
            name='allowed_loop_types',
        ),
        migrations.RemoveField(
            model_name='evaluationcriteria',
            name='max_loop_iterations',
        ),
        migrations.CreateModel(
            name='StudentPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strength_areas', models.JSONField(default=dict)),
                ('weakness_areas', models.JSONField(default=dict)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
