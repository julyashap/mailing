import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from mailing.management.commands.send_mail import send_mail

logger = logging.getLogger(__name__)


# логика периодической отправки письма (зависит от дат, меняет статус и тд)
class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_mail,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="send_mail",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_mail'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")