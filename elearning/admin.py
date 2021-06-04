from django.contrib import admin
from .models import Staff, Check, Course, Sub_Course, Course_Pretest, Staff_Score, Staff_Vdolog, Feedback, Evaluate_t, Closed_class, Hub_test

# Register your models here.
admin.site.register(Staff)
admin.site.register(Check)
admin.site.register(Course)
admin.site.register(Sub_Course)
admin.site.register(Course_Pretest)
admin.site.register(Staff_Score)
admin.site.register(Staff_Vdolog)
admin.site.register(Feedback)
admin.site.register(Evaluate_t)
admin.site.register(Closed_class)
admin.site.register(Hub_test)

