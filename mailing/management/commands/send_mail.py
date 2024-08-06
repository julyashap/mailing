from django.core.management.base import BaseCommand

from mailing.services import sending_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        sending_mail()
