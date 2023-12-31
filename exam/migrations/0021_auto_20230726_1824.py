# Generated by Django 3.0.5 on 2023-07-26 12:54

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0020_remove_question_blankans'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='question',
            managers=[
                ('objects_of_dm', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='qtag',
            field=models.CharField(blank=True, choices=[('Decision-making', 'Decision-making'), ('Emotional Intelligence', 'Emotional Intelligence')], max_length=200, null=True),
        ),
    ]
