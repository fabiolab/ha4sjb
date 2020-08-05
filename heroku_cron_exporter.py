from apscheduler.schedulers.blocking import BlockingScheduler
from exporter import ha2google

sched = BlockingScheduler()


@sched.scheduled_job('interval', days=1)
def scheduled_job():
    ha2google()


sched.start()
