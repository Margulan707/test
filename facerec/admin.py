from django.contrib import admin
from. models import Check
from. models import Day, WorkShift, Issue


# Register your models here.
admin.site.register(Check)
admin.site.register(Day)
admin.site.register(WorkShift)
admin.site.register(Issue)