# Generated by Django 5.1.3 on 2025-02-09 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorting_feedback', '0010_deadlineextensionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationcriteria',
            name='title',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
