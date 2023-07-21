# Generated by Django 3.0.5 on 2023-07-21 11:19

from django.db import migrations, models
import exam.models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0018_question_blankans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='audio',
        ),
        migrations.AddField(
            model_name='question',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to=exam.models.get_audio_upload_path),
        ),
    ]
