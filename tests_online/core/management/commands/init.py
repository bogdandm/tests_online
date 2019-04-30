import logging
import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = _("Create superuser (username and password are the same as DB ones)")
    enabled = os.environ.get("AUTO_INIT", "False") == "True"

    def handle(self, *args, **options):
        if self.enabled:
            logger.info("Creating superuser...")
            User = get_user_model()
            if not User.objects.exists():
                User.objects.create_superuser(
                    username=os.environ.get("POSTGRES_USER"),
                    email=None,
                    password=os.environ.get("POSTGRES_PASSWORD"),
                )
