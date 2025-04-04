# Generated by Django 5.1 on 2025-02-11 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NYSCAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', models.IntegerField()),
                ('batch', models.CharField(max_length=200)),
                ('stream', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=200)),
                ('state_code', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id'],
                'indexes': [models.Index(fields=['-id'], name='nysc_church_id_1af385_idx')],
            },
        ),
        migrations.CreateModel(
            name='NYSCNewComer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('phone', models.IntegerField()),
                ('batch', models.CharField(max_length=200)),
                ('stream', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=200)),
                ('state_code', models.CharField(max_length=200)),
                ('dob', models.DateField()),
                ('department', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id'],
                'indexes': [models.Index(fields=['-id'], name='nysc_church_id_141cdd_idx')],
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.CharField(max_length=200)),
                ('stream', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-id'],
                'indexes': [models.Index(fields=['-id'], name='nysc_church_id_6c575c_idx')],
            },
        ),
    ]
