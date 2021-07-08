import pendulum
from apscheduler.schedulers.blocking import BlockingScheduler
from exporter import ha2google

sched = BlockingScheduler()


@sched.scheduled_job('interval', hours=1)
def scheduled_job():
    ha2google()


# Start import one minute before deploy
one_minute_delay = pendulum.now().add(minutes=1)  # Let time for the server to start
sched.add_job(
    ha2google,
    trigger="cron",
    year=one_minute_delay.year,
    month=one_minute_delay.month,
    day=one_minute_delay.day,
    hour=one_minute_delay.hour,
    minute=one_minute_delay.minute,
)

sched.start()
