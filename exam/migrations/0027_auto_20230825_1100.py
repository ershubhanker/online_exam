# Generated by Django 3.0.5 on 2023-08-25 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0026_result_time_taken_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='predict_attrition',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='predict_performance',
            field=models.TextField(blank=True, null=True),
        ),
    ]
