from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserAnswers(models.Model):
    choices = models.ManyToManyField('questions.Answer', related_name="+", verbose_name=_("Answers"))

    test = models.ForeignKey('questions.Test', models.CASCADE, related_name="answers_set", verbose_name=_("Test"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name="answers_set",
                             verbose_name=_("User"))

    def __str__(self):
        return f"{self.test.title}, {self.user}"

    class Meta:
        verbose_name = _("User answers")
        verbose_name_plural = _("Users answers")
