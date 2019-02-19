from django.contrib import admin

# Register your models here.
from .models import Worker
from .models import Schedules
from .models import Positions
from .models import Standard


admin.site.register(Worker)
admin.site.register(Schedules)
admin.site.register(Positions)
admin.site.register(Standard)