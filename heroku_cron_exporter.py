from apscheduler.schedulers.blocking import BlockingScheduler
from exporter import ha2google

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def scheduled_job():
    ha2google()


sched.start()
