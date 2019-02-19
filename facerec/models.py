from django.db import models
from workrkopt.models import Worker
from  django.utils import timezone
from datetime import datetime, date, timedelta
import time
class Day(models.Model):

	
	Day = models.DateField(null = True)

	Worker = models.ForeignKey(Worker,
							on_delete=models.CASCADE, default = 0)

	Total_Time = models.DurationField(null = True,  default = timedelta(0))

	Worked_Time = models.DurationField(null = True, default = timedelta(0))

	Late_Come = models.DurationField(null = True, default = timedelta(0))

	Early_Leave = models.DurationField(null = True, default = timedelta(0))

	Status = models.CharField(max_length = 100, null = True)

	Mismatch = models.BooleanField(default = False)

	def save(self, *args, **kwargs):
		print('Save method executed!')
		super().save(*args, **kwargs)
		workshifts = WorkShift.objects.filter(Worker = self.Worker, Day = self)
		if not workshifts:
			day = {'0':'Monday',
					'1':'Tuesday',
					'2':'Wednesday',
					'3':'Thursday',
					'4':'Friday',
					'5':'Saturday',
					'6':'Sunday'}
			if (getattr(self.Worker.Schedule,str(day[str(datetime.today().weekday())])) and self.Worker.Working):
				day_time = getattr(self.Worker.Schedule,str(day[str(datetime.today().weekday())]))
				times = day_time.split(";")
				total_time_day = timedelta(0)
				for time in times: 
					start_time = datetime.strptime(time.split("-")[0], '%H:%M').time()
					finish_time = datetime.strptime(time.split("-")[1], '%H:%M').time()
					total_time = datetime.combine(date.min, finish_time) - datetime.combine(date.min, start_time)
					total_time_day += total_time
					
					workshift=WorkShift(Worker = self.Worker, Day = self, Start_Time=start_time, Finish_Time=finish_time, Total_Time = total_time)
					workshift.save()
				print(total_time_day)
				self.Total_Time = total_time_day
				self.save()
			else:
				self.Total_Time = timedelta(0)
		super().save(*args, **kwargs)
	def Update_Times(self):
		print(self.Worked_Time)
		self.Worked_Time = timedelta(0)
		self.Late_Come = timedelta(0)
		self.Early_Leave = timedelta(0)
		for workshift in self.workshift.all():
			self.Worked_Time += workshift.Worked_Time
			self.Late_Come  += workshift.Late_Come
			self.Early_Leave  += workshift.Early_Leave
		self.Worked_Time = self.Worked_Time
		self.Late_Come = self.Late_Come
		self.Early_Leave = self.Early_Leave
		print(self)
		self.save()
			
	def __str__(self):
		return str(self.Worker.Name + self.Worker.Surname  + " " + str(self.Day))

class WorkShift(models.Model):
	Worker = models.ForeignKey(Worker,
							on_delete=models.CASCADE, default = 0)

	Day = models.ForeignKey(Day,
							on_delete=models.CASCADE, default = 0, related_name = 'workshift')

	Start_Time = models.TimeField(null = True,  default = "00:00:00")

	Finish_Time = models.TimeField(null = True,  default = "00:00:00")

	Total_Time = models.DurationField(null = True,  default = timedelta(0))

	Worked_Time = models.DurationField(null = True, default = timedelta(0))

	Late_Come = models.DurationField(null = True,  default = timedelta(0))

	Early_Leave = models.DurationField(null = True,  default = timedelta(0))

	def __str__(self):
		return str(self.Worker.Name + self.Worker.Surname  + " " + str(self.Day))

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.Day.Update_Times()
class Check(models.Model):
	
	Worker = models.ForeignKey(Worker,
							on_delete=models.CASCADE, default = None, null = True)

	Day = models.ForeignKey(Day,
							on_delete=models.CASCADE, default = None, null = True)

	WorkShift = models.ForeignKey(WorkShift,
							on_delete=models.CASCADE, default = None, null = True)

	date = models.DateTimeField(default = timezone.now)

	Status = models.BooleanField(null = True)

	def save(self, *args, **kwargs):

		super().save(*args, **kwargs)
		day = {'0':'Mon',
				'1':'Tue',
				'2':'Wed',
				'3':'Thu',
				'4':'Fri',
				'5':'Sat',
				'6':'Sun',}

		if (self.Status == 1):
			self.Day.Status = "Working"
			self.Worker.Last_Check_In = self
			self.Day.save()
			
		if (self.Status == 0):
			self.Day.Status = "Not_Working"
			self.Day.save()
			if (self.Worker.Last_Check_In.WorkShift != self.WorkShift or (self.Worker.Last_Check_In.WorkShift == None and self.WorkShift == None)):
				self.Day.Mismatch = True 
				self.Day.save()
				issued_worked_time = self.date - self.Worker.Last_Check_In.date
				issued_worked_time -= timedelta(microseconds=issued_worked_time.microseconds)
				print(issued_worked_time)
				issue = Issue(Worker = self.Worker, Day = self.Day, Start_Time = self.Worker.Last_Check_In.date, Finish_Time = self.date, Worked_Time = issued_worked_time)
				if ((self.Worker.Last_Check_In.WorkShift == None and self.WorkShift != None) or (self.Worker.Last_Check_In.WorkShift == None and self.WorkShift == None)):
					issue.Status = "Non-Working Time"
				elif(self.Worker.Last_Check_In.WorkShift != None and self.WorkShift != None):
					issue.Status = "Forgot to Check Out"

				issue.save()
			else :
				self.WorkShift.Worked_Time += (datetime.combine(date.min, self.date.time()) - datetime.combine(date.min, self.Worker.Last_Check_In.date.time()))
				self.WorkShift.save()
		super().save(*args, **kwargs)


class Issue (models.Model): 
	Worker = models.ForeignKey(Worker,
							on_delete=models.CASCADE, default = 0)

	Day = models.ForeignKey(Day,
							on_delete=models.CASCADE, default = 0)

	Worked_Time = models.DurationField(null = True, default = timedelta(0))

	Start_Time = models.DateTimeField(null = True,  default = "00:00:00")

	Finish_Time = models.DateTimeField(null = True,  default = "00:00:00")
	
	Status = models.CharField(max_length = 100, null = True)
	
	Solved = models.BooleanField(default = False)

	def __str__(self):
		return str(self.Worker.Name + self.Worker.Surname  + " " + str(self.Day))