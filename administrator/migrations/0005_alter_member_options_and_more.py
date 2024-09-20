# Generated by Django 4.2.7 on 2024-02-06 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0004_alter_department_options_alter_member_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveIndex(
            model_name='member',
            name='administrat_date_17349a_idx',
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['-date'], name='administrat_date_2f6444_idx'),
        ),
    ]
