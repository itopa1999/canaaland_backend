from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Member)
admin.site.register(Department)
admin.site.register(Question)
admin.site.register(Attendance)


admin.site.register(Tracking)