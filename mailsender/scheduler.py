import logging

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from mailsender.services import send_mailing


logger = logging.getLogger(__name__)


def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        send_mailing,
        IntervalTrigger(minutes=1),
        id='send_mailing',
        name='Send mailing every minute',
        replace_existing=True
    )
    scheduler.start()

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
