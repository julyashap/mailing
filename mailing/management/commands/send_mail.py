from django.core.management.base import BaseCommand


# логика отправки письма (независимо от дат и всего прочего)
def send_mail():
    pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
