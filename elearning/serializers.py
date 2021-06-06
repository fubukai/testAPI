from django.contrib.auth import models
from .models import Staff, Check, Course, Sub_Course, Course_Pretest, Staff_Score, Staff_Vdolog, Feedback, Evaluate_t, Closed_class, Hub_test
from rest_framework import serializers


class request_Sub_Course(serializers.ModelSerializer):
	class Meta:
		model = Sub_Course
		fields = ['Title','ConstructorName', 'ConstructorPosition','Tel','email','Document','URLGdrive']

class request_Course(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = ['CourseName','CourseBy', 'CourseStatus']