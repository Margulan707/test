from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
import base64
from PIL import Image
import cv2
import io
import numpy as np
import face_recognition
from workrkopt.models import Worker
from django.contrib.auth import logout
from. models import Check, Day, WorkShift
import json
from datetime import datetime, date
# Create your views here.
def facerec_main(request):
	return render(request, 'facerec/facerec_main.html')

def facerec(request):
	if request.method == 'POST': 
		status = request.POST['check_status']
		image = request.POST['the_image']
		image = image.split(',')[1]
		im = Image.open(io.BytesIO(base64.b64decode(image)))
		image_cv = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)
		face_locations = face_recognition.face_locations(image_cv)
		face_encodings = face_recognition.face_encodings(image_cv, face_locations)
		known_face_encodings = []
		known_face_pk = []
		for worker in Worker.objects.filter(user = request.user):
			temp = worker.Face_Encodings.split("[")[2].split("]")[0]
			known_face_encoding = np.fromstring(temp, dtype=float, sep=',')
			known_face_encodings.append(known_face_encoding)
			known_face_pk.append(worker.pk)
		if len(face_encodings) == 1: 
			face_count_error = False
			for face_encoding in face_encodings:
				matches = face_recognition.face_distance(known_face_encodings, face_encoding)				
				name_index = np.argmin(matches)
				if (matches[name_index]<0.5):
					checked_worker = Worker.objects.get(pk=known_face_pk[name_index])
					workshifts = WorkShift.objects.filter(Worker = Worker.objects.get(pk=known_face_pk[name_index]), 
														Day = Day.objects.get(Day = str(datetime.today().strftime('%Y-%m-%d')),
															Worker = Worker.objects.get(pk=known_face_pk[name_index])))
					today_Day = Day.objects.get(Worker = checked_worker, Day = str(datetime.today().strftime('%Y-%m-%d')))
					if (checked_worker.Work_Status): 
						if (status == "1"):
							data = {'status_message': '0',
									'message': 'Вы уже вошли'}
							return HttpResponse(json.dumps(data))
						else:
							current_workshift = None
							if len(workshifts)>0: 
								for workshift in workshifts: 
									if datetime.now().time()>workshift.Start_Time:
										current_workshift = WorkShift.objects.get(Worker = checked_worker, 
															  Day = today_Day, Finish_Time=workshift.Finish_Time)
										BorderTime = current_workshift.Finish_Time
										if ( BorderTime > datetime.now().time()):
											timedelta = datetime.combine(date.min, BorderTime) - datetime.combine(date.min, datetime.now().time())
											current_workshift.Early_Leave =  timedelta
											
											current_workshift.save()
										
										today_Day.Early_Leave
										today_Day.save()
										 
							check = Check(Worker = checked_worker,
									WorkShift = current_workshift,
									Day = today_Day,
									Status = 0)
							check.save()
							checked_worker.Work_Status = False
							checked_worker.save()
							data = {'status_message': '1',
								'Name': checked_worker.Name,
								'check_pk': check.pk,
								'message': 'Хорошего вам вечера!'}
							return HttpResponse(json.dumps(data))
					else: 
						if (status =="1"): 
							current_workshift = None 
							if len(workshifts)>0: 
								for workshift in workshifts: 
									if datetime.now().time()<workshift.Finish_Time:
										current_workshift = WorkShift.objects.get(Worker = Worker.objects.get(pk=known_face_pk[name_index]), 
																			Day = Day.objects.get(Day = str(datetime.today().strftime('%Y-%m-%d')),
																				Worker = Worker.objects.get(pk=known_face_pk[name_index])), 
																			Finish_Time=workshift.Finish_Time)
										if len(Check.objects.filter(WorkShift = current_workshift, Status = 1))==0: 
											BorderTime = current_workshift.Start_Time
											if (datetime.now().time()>BorderTime):
												timedelta = datetime.combine(date.min, datetime.now().time()) - datetime.combine(date.min, BorderTime)
												current_workshift.Late_Come = timedelta 
												current_workshift.save()
										break

							check = Check(Worker = checked_worker,
										WorkShift = current_workshift,
										Day = today_Day,
										Status = 1)
							check.save()
							checked_worker.Work_Status = True
							checked_worker.save()
							data = {'status_message': '2',
									'Name': checked_worker.Name,
									'check_pk': check.pk,
									'message': 'Добро Пожаловать!'}
							return HttpResponse(json.dumps(data))
						else: 
							data = {'status_message': '3',
									'message': 'Первым делом войдите'}
							return HttpResponse(json.dumps(data))


				else:
					data = {'status_message': '4',
							'message': 'Лицо не распознано'}
					return HttpResponse(json.dumps(data))
		else:
			data = {'status_message': '5',
					'message': 'Лицо не найдено'}
			return HttpResponse(json.dumps(data))



def check_delete(request): 
	if request.method == "POST": 
		pk_delete = request.POST['pk_delete']
		Check.objects.filter(pk = int(pk_delete)).delete()
		return HttpResponse("deleted")


