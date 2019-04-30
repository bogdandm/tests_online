from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserAnswers(models.Model):
    choices = models.ManyToManyField('questions.Answer', verbose_name=_("Answers"))

    test = models.ForeignKey('questions.Test', models.CASCADE, verbose_name=_("Test"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_("User"))

    class Meta:
        verbose_name = _("User answers")
        verbose_name_plural = _("Users answers")
