# Generated by Django 4.2.7 on 2024-02-20 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0012_alter_attendance_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=200, null=True)),
                ('action', models.CharField(blank=True, max_length=2000, null=True)),
                ('color', models.CharField(blank=True, max_length=10, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-date'],
                'indexes': [models.Index(fields=['-date'], name='administrat_date_6a68bf_idx')],
            },
        ),
    ]
