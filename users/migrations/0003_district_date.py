# Generated by Django 4.2.7 on 2024-02-20 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_department_district_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
