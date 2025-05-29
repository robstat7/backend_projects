from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	username = models.CharField(max_length=300, unique=True)
	email = models.EmailField(max_length=400, unique=True)
	password = models.CharField(max_length=300)

class ToDo(models.Model):
	title = models.CharField(max_length=300)
	description = models.TextField()
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

