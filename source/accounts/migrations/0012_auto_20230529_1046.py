# Generated by Django 2.2.17 on 2023-05-29 04:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20230526_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='trial_valid_until',
            field=models.DateField(default=datetime.date(2023, 6, 13)),
        ),
    ]
