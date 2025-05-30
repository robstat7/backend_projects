from django.db import models

class Secret(models.Model):
  text = models.TextField()
  created_on = models.DateTimeField(auto_now_add=True)
  uri = models.CharField(max_length=200)
  uri_random_text = models.CharField(max_length=100)
