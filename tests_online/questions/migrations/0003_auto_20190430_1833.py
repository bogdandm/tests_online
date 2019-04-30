# Generated by Django 2.2 on 2019-04-30 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20190430_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='questions.Question', verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='questions.Test', verbose_name='Test'),
        ),
        migrations.AlterField(
            model_name='useranswers',
            name='choices',
            field=models.ManyToManyField(related_name='_useranswers_choices_+', to='questions.Answer', verbose_name='Answers'),
        ),
        migrations.AlterField(
            model_name='useranswers',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_set', to='questions.Test', verbose_name='Test'),
        ),
        migrations.AlterField(
            model_name='useranswers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_set', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]