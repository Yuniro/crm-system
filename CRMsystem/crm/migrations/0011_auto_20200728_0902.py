# Generated by Django 3.0.8 on 2020-07-28 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_auto_20200724_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='is_owner',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]