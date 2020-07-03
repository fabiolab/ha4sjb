from apscheduler.schedulers.blocking import BlockingScheduler
from exporter import ha2google

sched = BlockingScheduler()


# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
@sched.scheduled_job('interval', hours=3)
def scheduled_job():
    ha2google()


sched.start()
