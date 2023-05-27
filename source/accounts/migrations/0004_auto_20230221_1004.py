# Generated by Django 2.2.17 on 2023-02-21 04:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20201124_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('duration', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('features', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='activation',
            name='subscription_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Subscription'),
        ),
        migrations.AlterField(
            model_name='activation',
            name='trial_valid_until',
            field=models.DateField(default=datetime.date(2023, 3, 8)),
        ),
    ]