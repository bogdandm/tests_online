# Generated by Django 2.2.1 on 2019-05-16 15:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('questions', '0008_auto_20190516_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='params_value',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, size=None,
                                                            verbose_name='Parameters'),
        ),
    ]
