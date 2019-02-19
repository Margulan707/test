from django.db import models
from  django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
import cv2
import face_recognition
from datetime import datetime, timedelta, date
# Create your models here.

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'user_{0}/{1}'.format(instance.user.id, filename)


def make_face_endogings(url):
	img = cv2.imread(str(settings.MEDIA_ROOT)+"/"+str(url))
	face_locations = face_recognition.face_locations(img)
	face_encodings = face_recognition.face_encodings(img, face_locations)
	return face_encodings


class Positions(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.CASCADE)
	Name = models.CharField(max_length = 100)	
	def number_of_workers(self):
			return len(Worker.objects.filter(Position = '{}'.format(self.pk)))

	def __str__(self):
		return self.Name


class Schedules(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.CASCADE)
	
	Name = models.CharField(max_length = 100)
	Monday = models.CharField(max_length = 100, null=True, blank=True, default=None)
	Tuesday = models.CharField(max_length = 100, null=True, blank=True, default=None)
	Wednesday = models.CharField(max_length = 100, null=True, blank=True, default=None)
	Thursday = models.CharField(max_length = 100, null=True, blank=True, default=None)
	Friday = models.CharField(max_length = 100, null=True, blank=True, default=None)
	Saturday = models.CharField(max_length = 100, null=True, blank=True, default=None)
	Sunday = models.CharField(max_length = 100, null=True, blank=True, default=None)


	def __str__(self):
		return self.Name

class Standard(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.CASCADE, 
							null=True)
	Name = models.CharField(max_length = 100, null=True)
	Late_Come = models.TimeField(default = "00:00", verbose_name= ('Допустимое время опоздания'))
	Early_Leave = models.TimeField(default = "00:00", verbose_name= ('Допустимое время раннего ухода'))

	def __str__(self):
		return self.Name


class Worker(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.CASCADE, 
							null=True)
	
	GENDERS = (
		('М', 'Мужчина'),
		('Ж', 'Женщина'))
	
	Name = models.CharField(max_length = 100)
	Surname = models.CharField(max_length = 100)
	Gender = models.CharField(max_length = 100, choices=GENDERS)
	BirthDate = models.DateTimeField(max_length = 100)
	Phone = models.CharField(max_length = 100)
	Email = models.CharField(max_length = 100)
	Position = models.ForeignKey(Positions, on_delete = models.SET_NULL, null = True,  related_name = 'worker')
	Schedule = models.ForeignKey(Schedules, on_delete = models.SET_NULL, null = True)
	Standard = models.ForeignKey(Standard, on_delete = models.SET_NULL, null = True)
	Photo = models.FileField(upload_to=user_directory_path, default = "default.jpg")
	Working = models.BooleanField(default = False)
	Face_Encodings = models.CharField(max_length = 10000, blank = True)
	Work_Status = models.BooleanField(default = False)
	Last_Check_In = models.OneToOneField('facerec.Check', on_delete=models.SET_NULL, null = True, default = None)
	def last_month_info(self):

		def daterange(start_date, end_date):
			for n in range(int ((end_date - start_date).days)):
				yield start_date + timedelta(n)

		start_date = datetime.today().replace(day=1)
		today = datetime.now()
		total_time = 0 
		total_time_worked = 0
		total_time_late = 0
		total_time_early = 0
		total_efficiency = 0
		day = {'0':'Mon',
				'1':'Tue',
				'2':'Wed',
				'3':'Thu',
				'4':'Fri',
				'5':'Sat',
				'6':'Sun',}


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.Face_Encodings = make_face_endogings(self.Photo)
		super().save(*args, **kwargs)


	def get_absolute_url(self):
		return reverse('worker-detail', kwargs = {'pk': self.pk})




