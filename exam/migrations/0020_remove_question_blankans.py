# Generated by Django 3.0.5 on 2023-07-21 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0019_auto_20230721_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='blankans',
        ),
    ]