import hashlib
import uuid
from enum import Enum

from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


def unique_hash() -> str:
    return hashlib.sha256(uuid.uuid4().bytes).hexdigest()


class TestStatsChoices(Enum):
    OFF = "off"
    ANY = "any"
    AUTHORIZED_ONLY = "auth_only"
    PRIVATE = "private"


def _params__default():
    return ["SCORE"]


def _params_defaults__default():
    return ["SCORE"]


class Test(models.Model):
    hash = models.CharField(_("Hash"), max_length=64, default=unique_hash, db_index=True, unique=True)
    title = models.CharField(_("Title"), max_length=256)
    description = models.TextField(_("Description"))
    is_private = models.BooleanField(_("Is private?"), default=False)

    params = pg_fields.ArrayField(models.CharField(max_length=32), default=_params__default,
                                  verbose_name=_("Parameters"))
    params_defaults = pg_fields.ArrayField(models.FloatField(), default=_params_defaults__default,
                                           verbose_name=_("Parameters default values"))

    stats_restriction = models.CharField(_("Statistic restriction"), choices=[(x, x.value) for x in TestStatsChoices],
                                         max_length=16, default=TestStatsChoices.OFF)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_("Owner"))

    def clean(self):
        if len(self.params) != len(self.params_defaults):
            raise ValidationError(_("Length of `params` and `params_defaults` fields should be equal"))

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
