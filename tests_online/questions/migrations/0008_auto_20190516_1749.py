# Generated by Django 2.2.1 on 2019-05-16 14:49

import django.contrib.postgres.fields
from django.db import migrations, models

import questions.models.test


class Migration(migrations.Migration):
    dependencies = [
        ('questions', '0007_auto_20190513_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='params',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), blank=True,
                                                            default=questions.models.test._params__default, size=None,
                                                            verbose_name='Parameters'),
        ),
        migrations.AlterField(
            model_name='test',
            name='params_defaults',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True,
                                                            default=questions.models.test._params_defaults__default,
                                                            size=None, verbose_name='Parameters default values'),
        ),
    ]
