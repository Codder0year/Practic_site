import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management import BaseCommand
from mailsender.services import send_mailing


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_job(
            send_mailing,
            IntervalTrigger(minutes=1),
            id='send_mailing',
            name='Send mailing every minute',
            replace_existing=True
        )
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")