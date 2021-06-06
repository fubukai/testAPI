from django.db import models

# Create your models here.
class User(models.Model):
	url = models.CharField(max_length=500,null=True)
	username = models.CharField(max_length=500,null=True)
	email = models.CharField(max_length=500,null=True)
	groups  = models.CharField(max_length=500,null=True)

class Group(models.Model):
	url = models.CharField(max_length=500,null=True)
	name = models.CharField(max_length=500,null=True)