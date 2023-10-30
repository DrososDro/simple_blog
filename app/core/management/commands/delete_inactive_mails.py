"""
Django command Delete all mails that dont activate within one hour.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    """Django command ."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Starting deleting mails")
        users = get_user_model().objects.filter(is_active=False)

        if users:
            for user in users:
                if timezone.now() >= user.created_at + timedelta(hours=1):
                    user.delete()

                    self.stdout.write(
                        self.style.SUCCESS(
                            "Unactive emails Deleted successfully",
                        )
                    )
