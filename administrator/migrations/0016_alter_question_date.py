# Generated by Django 5.1 on 2024-09-20 21:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0015_alter_question_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 9, 20, 21, 12, 50, 908830, tzinfo=datetime.timezone.utc)),
        ),
    ]
