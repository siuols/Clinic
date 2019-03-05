from django.contrib import admin
from .models import Course, Department, Stock, Patient, History
# Register your models here.

admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Stock)
admin.site.register(Patient)
admin.site.register(History)