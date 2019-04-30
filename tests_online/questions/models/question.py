from django.db import models
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    position = models.IntegerField(_("Position"), default=-1)
    text = models.TextField(_("Text"))

    test = models.ForeignKey('questions.Test', related_name="questions", on_delete=models.CASCADE,
                             verbose_name=_("Test"))

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ("position",)

    def __str__(self):
        return self.text