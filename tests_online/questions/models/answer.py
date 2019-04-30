from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Answer(models.Model):
    position = models.IntegerField(_("Position"), default=-1)
    text = models.TextField(_("Text"))
    params_value = pg_fields.ArrayField(models.FloatField(), verbose_name=_("Parameters"), null=True)

    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, verbose_name=_("Question"))

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
