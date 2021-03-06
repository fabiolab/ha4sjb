from apscheduler.schedulers.blocking import BlockingScheduler
from exporter import ha2google

sched = BlockingScheduler()


@sched.scheduled_job('interval', hours=12)
def scheduled_job():
    ha2google()


sched.start()
