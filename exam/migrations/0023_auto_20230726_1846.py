# Generated by Django 3.0.5 on 2023-07-26 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0022_auto_20230726_1838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='decisionmakingquestion',
            old_name='question',
            new_name='ques',
        ),
        migrations.RenameField(
            model_name='emotionalintelligencequestion',
            old_name='question',
            new_name='ques',
        ),
    ]
