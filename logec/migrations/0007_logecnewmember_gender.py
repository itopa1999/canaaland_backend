# Generated by Django 5.1.6 on 2025-03-01 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logec', '0006_logecnewmember_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='logecnewmember',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=200, null=True),
        ),
    ]
