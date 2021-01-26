import os
from datetime import datetime, timedelta
from app import celery
from celery.decorators import periodic_task
from celery.task.schedules import crontab

from app.utils import unschedule_bus
from app.models import db



# app = celery.Celery('example')
# app.conf.update(
# 	BROKER_URL=os.environ.get('REDIS_URL', 'redis://localhost:6379'), 
# 	CELERY_RESULT_BACKEND=os.environ.get('REDIS_URL', 'redis://localhost:6379'), 
# 	)


# @app.task
# def add(x, y):
# 	print('+++++++++++++++ adding', x+y)
# 	return x + y


# @app.task
# def write_file(x, y):
# 	fh = open("/home/samuelitwaru/Desktop/JAMES/FILE.txt", 'a')
# 	fh.write('hello\n')
# 	fh.close()


@celery.task
def free_bus(bus):
	print("*******", bus)
	# unschedule_bus(bus)
	# db.session.commit()




free_bus.delay(12)



# @periodic_task(run_every=(crontab()), name="do", ignore_result=True)
# def do():
# 	# fh = open("/home/samuelitwaru/Desktop/JAMES/FILE.txt", 'a')
# 	# fh.write('hello\n')
# 	# fh.close()
# 	print(">>>>>>>>>>>>>>>>> hello")
# 	set_time = datetime.utcnow() + timedelta(seconds=15)
# 	print("now:", datetime.utcnow(), set_time, datetime)
# 	result = write_file.apply_async((2, 2), eta=set_time)
# 	add.delay(1,2)



