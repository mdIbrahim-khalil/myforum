# Generated by Django 2.2.17 on 2020-11-28 14:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20201124_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='trial_valid_until',
            field=models.DateField(default=datetime.date(2020, 12, 13)),
        ),
    ]
