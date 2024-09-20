# Generated by Django 4.2.7 on 2024-03-06 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretary', '0005_alter_transaction_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimony',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('email', models.EmailField(blank=True, max_length=500, null=True)),
                ('testimony', models.TextField(blank=True, max_length=1600, null=True)),
                ('approve', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['-date'],
                'indexes': [models.Index(fields=['-date'], name='secretary_t_date_3e54cf_idx')],
            },
        ),
        migrations.CreateModel(
            name='Sermon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('paragraph1', models.TextField(blank=True, max_length=5000, null=True)),
                ('paragraph2', models.TextField(blank=True, max_length=5000, null=True)),
                ('paragraph3', models.TextField(blank=True, max_length=5000, null=True)),
                ('paragraph4', models.TextField(blank=True, max_length=5000, null=True)),
                ('paragraph5', models.TextField(blank=True, max_length=5000, null=True)),
                ('paragraph6', models.TextField(blank=True, max_length=5000, null=True)),
                ('paragraph7', models.TextField(blank=True, max_length=5000, null=True)),
                ('paragraph8', models.TextField(blank=True, max_length=5000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['-date'],
                'indexes': [models.Index(fields=['-date'], name='secretary_s_date_bc987a_idx')],
            },
        ),
    ]
