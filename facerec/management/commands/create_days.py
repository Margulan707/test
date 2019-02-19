from workrkopt.models import Worker
from facerec.models import Check, Day, WorkShift
from datetime import datetime, date, timedelta

while True:
	yesterday = date.today() - timedelta(1)
	day = Day.objects.filter(Day = str(datetime.today().strftime('%Y-%m-%d')))
	if not day:
		for worker in Worker.objects.all():
			day = Day(Worker = worker, Day = datetime.today().strftime('%Y-%m-%d'))
			day.save()
			print('DAY for {} is created!'.format(worker.Name))
		for worker in Worker.objects.all():
			try: 
				workshifts = WorkShift.objects.filter(Day = Day.objects.get(Worker = worker, Day = (datetime.today()-timedelta(1)).strftime('%Y-%m-%d')))
				for workshift in workshifts: 
				
					today_workshift = WorkShift.objects.get(Worker = worker, Day = Day.objects.get(Worker = workshift.Worker, Day = datetime.today().strftime('%Y-%m-%d')), Start_Time = "00:00:00")
					if str(workshift.Finish_Time) == '23:59:00' and today_workshift.Start_Time and  workshift.Worker.Work_Status: 
						yesterday = date.today() - timedelta(1)
						check_out = Check(Day = Day.objects.get(Worker = worker, Day = ((datetime.today()-timedelta(1)).strftime('%Y-%m-%d'))), WorkShift = workshift, Worker = workshift.Worker, date = datetime.combine(yesterday, datetime.strptime("23:59:00", '%H:%M:%S').time()), Status =False)
						check_out.save()
						check_in = Check(Day = Day.objects.get(Worker = today_workshift.Worker, Day = datetime.today().strftime('%Y-%m-%d')), WorkShift = today_workshift, Worker = today_workshift.Worker, date = datetime.combine(date.today(), datetime.strptime("00:00:00", '%H:%M:%S').time()), Status =True)
						check_in.save()
			except: 
				pass