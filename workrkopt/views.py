from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from.models import Worker, Positions, Schedules, Standard
from facerec.models import Day
import json
from django.core import serializers
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from. forms import WorkerForm
from facerec.models import Check, Day, Issue, WorkShift
from datetime import datetime, timedelta, time, date
from django.shortcuts import redirect
from itertools import chain

def ReportView(request):
	if request.method == 'POST':
		date_1 = request.POST['date_1']
		date_2 = request.POST['date_2']
		workers = request.POST['workers']
		print(workers)
		print(date_1)
		print(date_2)
		data =[]
		workers = workers.split(',')
		i = 0
		for worker in workers:
			try:
				data.append(getWorkerStatistics(worker, date_1, date_2))
				worker_name = Worker.objects.get(pk=worker)
				worker_photo = str(worker_name.Photo.url)
				worker_name = str(worker_name.Name + " " + worker_name.Surname)
				data[i]['worker_name']= worker_name
				data[i]['photo_url'] = worker_photo
				i+=1
			except: 
				pass
		

	return HttpResponse(json.dumps(data))

def IssuePenaltyView(request):
	if request.method == 'POST':
		penalty = request.POST['penalty']
		pk = request.POST['pk']
		issue = Issue.objects.get(pk = pk)
		print(issue.Worked_Time)
		issue.Day.Worked_Time += issue.Worked_Time*(1-int(penalty)/100)
		print(issue.Day.Worked_Time)
		issue.Solved = True
		issue.Day.save()
		issue.save()
		data = {"pk": pk}
	return HttpResponse(json.dumps(data))


@login_required
def Reports(request):
	today = str(datetime.today().strftime('%Y-%d-%m'))
	first_month_day = str(datetime.today().replace(day=1).strftime('%Y-%d-%m'))
	context = {
		'today_date':today,
		'first_month_day':first_month_day,
		'positions': Positions.objects.filter(user = request.user).prefetch_related('worker')
	}
	return render(request, 'workrkopt/reports.html', context)



def getWorkerStatistics(pk, start_date, end_date): 
	def convert_timedelta_hours(duration): 
		days, seconds = duration.days, duration.seconds
		hours = days*24+seconds//3600
		return hours
	def convert_timedelta_minutes(duration): 
		days, seconds = duration.days, duration.seconds
		minutes = (seconds%3600)//60
		return minutes
	def convert_timedelta_seconds(duration): 
		days, seconds = duration.days, duration.seconds
		seconds= (seconds%60)
		return seconds



	number_of_days = 0
	Total_Time = timedelta(0)
	Total_Worked_Time = timedelta(0)
	Total_Average_Late_Come = timedelta(0)
	Total_Average_Early_Leave = timedelta(0)
	Total_Time_Theft = timedelta(0)
	time_zero = datetime.strptime('00:00:00', '%H:%M:%S')
	end_date = datetime.strptime(end_date, "%Y-%d-%m")
	data = {}
	d = datetime.strptime(start_date, "%Y-%d-%m")
	delta = timedelta(days=1)
	while d <= end_date:
		try:
			Total_Time += Day.objects.get(Worker = Worker.objects.get(pk=pk), Day = d.date()).Total_Time
			Total_Worked_Time += Day.objects.get(Worker = Worker.objects.get(pk=pk), Day = d.date()).Worked_Time
			Total_Average_Late_Come += Day.objects.get(Worker = Worker.objects.get(pk=pk), Day = d.date()).Late_Come
			Total_Average_Early_Leave += Day.objects.get(Worker = Worker.objects.get(pk=pk), Day = d.date()).Early_Leave
			number_of_days+=1
		except: 
			pass
		d += delta
	Total_Time_Theft = Total_Time - Total_Worked_Time
	Total_Average_Late_Come = Total_Average_Late_Come/number_of_days
	Total_Average_Early_Leave = Total_Average_Early_Leave/number_of_days
	data= {
		'Total_Time': '{} часов {} минут'.format(convert_timedelta_hours(Total_Time),convert_timedelta_minutes(Total_Time)),
		'Total_Worked_Time': '{} часов {} минут'.format(convert_timedelta_hours(Total_Worked_Time),convert_timedelta_minutes(Total_Worked_Time)),
		'Total_Time_Theft': '{} часов {} минут'.format(convert_timedelta_hours(Total_Time_Theft), convert_timedelta_minutes(Total_Time_Theft)),
		'Total_Average_Late_Come': '{} часов {} минут {} секунд'.format(convert_timedelta_hours(Total_Average_Late_Come), convert_timedelta_minutes(Total_Average_Late_Come),(Total_Average_Late_Come.seconds%60)),
		'Total_Average_Early_Leave': '{} часов {} минут {} секунд'.format(convert_timedelta_hours(Total_Average_Early_Leave), convert_timedelta_minutes(Total_Average_Early_Leave), (Total_Average_Early_Leave.seconds%60))
	}
	return data


def WorkerStatistics(request,pk):
	worker = Worker.objects.get(pk = pk)
	if request.method == 'POST':
		start_date = request.POST['date_1']
		end_date = request.POST['date_2']
		data = getWorkerStatistics(pk, start_date, end_date)


	return HttpResponse(json.dumps(data))

@login_required
def DashboardView(request):
	workers = Worker.objects.filter(user = request.user)
	days = []
	issues = []
	day = {'0':'Monday',
					'1':'Tuesday',
					'2':'Wednesday',
					'3':'Thursday',
					'4':'Friday',
					'5':'Saturday',
					'6':'Sunday'}
	for worker in workers:
		issues = list(chain(issues, Issue.objects.filter(Worker = worker, Solved = False))) 
		try:
			if getattr(worker.Schedule, str(day[str(datetime.today().weekday())])):
				days.append(Day.objects.get(Worker = worker, Day = str(datetime.today().strftime('%Y-%m-%d'))))
		except:
			pass
	today = str(datetime.today().strftime('%Y-%d-%m'))
	context = {
		'days': days,
		'issues': issues,
		'positions': Positions.objects.all()
	}
	return render(request, 'workrkopt/dashboard.html', context)

def DetailedWorkerView(request):
	def convert_timedelta_hours(duration): 
		days, seconds = duration.days, duration.seconds
		hours = days*24+seconds//3600
		return hours
	def convert_timedelta_minutes(duration): 
		days, seconds = duration.days, duration.seconds
		minutes = (seconds%3600)//60
		return minutes
	def convert_timedelta_seconds(duration): 
		days, seconds = duration.days, duration.seconds
		seconds= (seconds%60)
		return seconds

	if request.method == 'POST':
		pk_day = request.POST['pk_day']
		day = Day.objects.get(pk=pk_day)
		workshifts = WorkShift.objects.filter(Day=day) 
		Name = str(day.Worker.Name +" " +day.Worker.Surname)
		image = str(day.Worker.Photo.url)
		Total_Time = day.Total_Time
		Total_Worked_Time = day.Worked_Time
		Total_Late_Come = day.Late_Come
		Total_Early_Leave = day.Early_Leave
		Total_Time_Theft = day.Total_Time - day.Worked_Time
		Start_Times = ""
		Finish_Times = ""
		Status = ""
		Total_Times = ""
		Total_Worked_Times = ""
		Worker_Comes = ""
		Worker_Leaves = ""
		Late_Comes = ""
		Early_Leaves = ""
		number_workshifts = 0
		number_worked_workshifts = 0
		for workshift in workshifts: 
				number_workshifts+=1
				Start_Times += str(workshift.Start_Time.replace(microsecond=0))+";"
				Finish_Times += str(workshift.Finish_Time.replace(microsecond=0))+";"
				if (Check.objects.filter(WorkShift = workshift, Status=True)):
					Worker_Comes += str(list(Check.objects.filter(WorkShift = workshift, Status=True))[0].date.time().replace(microsecond=0))+";"
				else: 
					Worker_Comes+="no_check;"
				if (Check.objects.filter(WorkShift = workshift, Status=False)):
					Worker_Leaves += str(list(Check.objects.filter(WorkShift = workshift, Status=False))[-1].date.time().replace(microsecond=0))+";"
				else:
					Worker_Leaves+="no_check;"
				Late_Comes += str(workshift.Late_Come-timedelta(microseconds = workshift.Late_Come.microseconds))+";"
				Early_Leaves += str(workshift.Early_Leave-timedelta(microseconds = workshift.Early_Leave.microseconds))+";"
				number_worked_workshifts+=1
		print(Worker_Leaves)
		print(Worker_Comes)
		data = {
				'Name':Name,
				'image': image,
				'number_workshifts':number_workshifts,
				'number_worked_workshifts':number_worked_workshifts,
				'Total_Time': '{} часов {} минут'.format(convert_timedelta_hours(Total_Time),convert_timedelta_minutes(Total_Time)),
				'Total_Worked_Time': '{} часов {} минут'.format(convert_timedelta_hours(Total_Worked_Time),convert_timedelta_minutes(Total_Worked_Time)),
				'Start_Times':Start_Times,
				'Finish_Times':Finish_Times,
				'Total_Times':Total_Times,
				'Total_Worked_Times':Total_Worked_Times,
				'Worker_Comes':Worker_Comes,
				'Worker_Leaves':Worker_Leaves,
				'Late_Comes':Late_Comes,
				'Early_Leaves':Early_Leaves,
				'Total_Late_Come': '{} часов {} минут {} секунд'.format(convert_timedelta_hours(Total_Late_Come), convert_timedelta_minutes(Total_Late_Come),(Total_Late_Come.seconds%60)),
				'Total_Early_Leave': '{} часов {} минут {} секунд'.format(convert_timedelta_hours(Total_Early_Leave), convert_timedelta_minutes(Total_Early_Leave), (Total_Early_Leave.seconds%60)),
				'Total_Time_Theft': '{} часов {} минут'.format(convert_timedelta_hours(Total_Time_Theft), convert_timedelta_minutes(Total_Time_Theft))
		
		}

	return HttpResponse(json.dumps(data))

@login_required
def CategoriesView(request):
	
	context = {
		'positions': Positions.objects.filter(user = request.user),
	}

	return render(request, 'workrkopt/positions_view.html', context)

@login_required
def WorkersView(request):
	context = {
		'workers': Worker.objects.filter(user = request.user),
		'positions': Positions.objects.all()
	}

	return render(request, 'workrkopt/home.html', context)

@login_required
def WorkerDetailView(request, pk):
	worker = Worker.objects.get(pk = pk)
	today = str(datetime.today().strftime('%Y-%d-%m'))
	first_month_day = str(datetime.today().replace(day=1).strftime('%Y-%d-%m'))
	data = getWorkerStatistics(pk, first_month_day, today)
	context = {
		'today_date':today,
		'first_month_day':first_month_day,
		'worker': Worker.objects.get(pk = pk),
		'checks': Check.objects.filter(Worker = Worker.objects.get(pk = pk)),
		'days': Day.objects.filter(Worker = Worker.objects.get(pk=pk))
	}
	context.update(data)
	worker.last_month_info()
	return render(request, 'workrkopt/worker_detail.html', context)



class WorkerChangeView(UpdateView):
	model = Worker
	fields = ['Name', 'Surname','Gender', 'BirthDate','Email','Phone','Position','Standard','Schedule','Photo','Working']	
	template_name_suffix = '_update_form'

@login_required
def WorkerCreateView(request):
	if request.method == 'POST':
		form = WorkerForm(request.user, request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			obj = form.save()
			return redirect('/monitoring/workers/')
		return render(request, 'workrkopt/worker_form.html', {'form': form})
	else:
		form = WorkerForm(request.user)
		return render(request, 'workrkopt/worker_form.html', {'form': form})
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(WorkerCreateView, self).form_valid(form)	
	
	

class WorkerDeleteView(DeleteView):	
	model = Worker
	#template_name_suffix='confirm-delete'
	success_url = reverse_lazy('home')


class PositionsChangeView(UpdateView):
	model = Positions
	fields = ['Name']	
	template_name_suffix = '_update_form'
	success_url = reverse_lazy('positions-view')

class PositionsCreateView(CreateView):
	model = Positions
	fields = ['Name']	
	success_url = reverse_lazy('positions-view')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(PositionsCreateView, self).form_valid(form)	

class PositionsDeleteView(DeleteView):
	model = Positions
	#template_name_suffix='positions_confirm_delete'
	success_url = reverse_lazy('positions-view')

@login_required
def SchedulesView(request):
	
	context = {
		'schedules': Schedules.objects.filter(user = request.user),
	}

	return render(request, 'workrkopt/schedules_view.html', context)
class SchedulesChangeView(UpdateView):
	model = Schedules
	
	fields = ['Name', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']	
	
	template_name_suffix = '_update_form'
	success_url = reverse_lazy('schedules-view')

class SchedulesCreateView(CreateView):
	model = Schedules
	fields = ['Name', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday']	
	success_url = reverse_lazy('schedules-view')
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(SchedulesCreateView, self).form_valid(form)	

class SchedulesDeleteView(DeleteView):
	model = Schedules
	#template_name_suffix='positions_confirm_delete'
	success_url = reverse_lazy('schedules-view')


@login_required
def StandardsView(request):
	
	context = {
		'standards': Standard.objects.filter(user = request.user),
	}

	return render(request, 'workrkopt/standards_view.html', context)

class StandardsChangeView(UpdateView):
	model = Standard
	fields = ['Name','Late_Come', 'Early_Leave']	
	template_name_suffix = '_update_form'
	success_url = reverse_lazy('standards-view')

class StandardsCreateView(CreateView):
	model = Standard
	fields = ['Name','Late_Come', 'Early_Leave']	
	success_url = reverse_lazy('standards-view')
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(StandardsCreateView, self).form_valid(form)	

class StandardsDeleteView(DeleteView):
	model = Standard
	#template_name_suffix='positions_confirm_delete'
	success_url = reverse_lazy('standards-view')