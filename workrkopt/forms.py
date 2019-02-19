from django import forms
from. models import Schedules, Worker, Standard, Positions

class WorkerForm(forms.ModelForm):
	def __init__(self, user, *args, **kwargs):
		super(WorkerForm, self).__init__(*args, **kwargs)
		self.fields['Schedule'].queryset = Schedules.objects.filter(user = user)
		self.fields['Standard'].queryset = Standard.objects.filter(user = user)
		self.fields['Position'].queryset = Positions.objects.filter(user = user)

	class Meta:
		model = Worker
		fields = ['Name', 'Surname','Gender', 'BirthDate','Email','Phone','Position','Standard','Schedule','Photo','Working']	
	