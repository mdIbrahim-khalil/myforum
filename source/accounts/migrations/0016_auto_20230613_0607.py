# Generated by Django 2.2.17 on 2023-06-13 00:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20230609_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='trial_valid_until',
            field=models.DateField(default=datetime.date(2023, 6, 28)),
        ),
    ]
