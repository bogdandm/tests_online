import hashlib
import uuid
from typing import List, Tuple

from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.memcached import memcached_property


def unique_hash() -> str:
    return hashlib.sha256(uuid.uuid4().bytes).hexdigest()


class TestStatsChoices:
    OFF = "off"
    ANY = "any"
    AUTHORIZED_ONLY = "auth_only"
    PRIVATE = "private"


def _params__default():
    return ["SCORE"]


def _params_defaults__default():
    return [1.0]


class Test(models.Model):
    class TestParamsError(ValidationError):
        def __init__(self, *fields):
            self.fields = fields
            super().__init__(_("Length of {} fields should be equal").format(fields))

        def __repr__(self):
            return 'TestParamsError(%s)' % self

    STATS_RESTRICTIONS_CHOICES = (
        (TestStatsChoices.OFF, _("Off")),
        (TestStatsChoices.ANY, _("Any")),
        (TestStatsChoices.AUTHORIZED_ONLY, _("Authorized only")),
        (TestStatsChoices.PRIVATE, _("Private"))
    )

    hash = models.CharField(_("Hash"), max_length=64, default=unique_hash, db_index=True, unique=True)
    title = models.CharField(_("Title"), max_length=256)
    description = models.TextField(_("Description"))
    is_private = models.BooleanField(_("Is private?"), default=False)

    params = pg_fields.ArrayField(models.CharField(max_length=256), default=_params__default,
                                  verbose_name=_("Parameters"))
    params_defaults = pg_fields.ArrayField(models.FloatField(), default=_params_defaults__default,
                                           verbose_name=_("Parameters default values"))

    stats_restriction = models.CharField(_("Statistic restriction"), max_length=16, default=TestStatsChoices.OFF,
                                         choices=STATS_RESTRICTIONS_CHOICES)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_("Owner"))

    @memcached_property(
        key=lambda test: str(test.id),
        timeout=60 ** 2  # 1 hour
    )
    def params_bounds(self) -> Tuple[List[float], List[float]]:
        params_min = [0.0 for param in self.params]
        params_max = params_min[:]
        for q in self.questions.only("id").iterator():
            params_values = list(zip(*q.answers.values_list("params_value", flat=True)))
            for i, param in enumerate(self.params):
                params_min[i] += min(params_values[i])
                params_max[i] += max(params_values[i])
        return params_min, params_max

    def clear_params_bounds(self):
        return self.__class__.params_bounds.fget.clear_cache(self)

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
        ordering = ("id",)

    def __str__(self):
        return self.title

    def clean(self):
        if len(self.params) != len(self.params_defaults):
            raise self.TestParamsError('params', 'params_defaults')
