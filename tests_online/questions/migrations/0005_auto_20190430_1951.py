# Generated by Django 2.2 on 2019-04-30 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20190430_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='position',
            field=models.SmallIntegerField(default=-1, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='question',
            name='position',
            field=models.SmallIntegerField(default=-1, verbose_name='Position'),
        ),
    ]
