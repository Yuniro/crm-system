# Generated by Django 3.1 on 2020-09-10 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0015_report_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information', models.TextField()),
            ],
        ),
    ]
