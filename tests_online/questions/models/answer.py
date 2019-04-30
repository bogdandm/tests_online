from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Answer(models.Model):
    position = models.SmallIntegerField(_("Position"), default=-1)
    text = models.TextField(_("Text"))
    params_value = pg_fields.ArrayField(models.FloatField(), verbose_name=_("Parameters"), null=True)

    question = models.ForeignKey('questions.Question', related_name="answers", on_delete=models.CASCADE,
                                 verbose_name=_("Question"))

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ("position",)

    def __str__(self):
        return f"{self.question} -> {self.text}"

    def clean(self):
        if len(self.params_value) != len(self.question.test.params_defaults):
            raise ValidationError(_("Length of `params_value` should be equal to length of `test.params`"))
