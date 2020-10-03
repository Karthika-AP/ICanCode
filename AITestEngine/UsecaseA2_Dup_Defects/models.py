from django.db import models

class File(models.Model):

  file = models.FileField(upload_to='Defects')
  filetype = models.CharField(max_length=200)
  project_id = models.IntegerField()

class File1(models.Model):

  file = models.FileField(upload_to='TestCase')
  filetype = models.CharField(max_length=200)
  project_id = models.IntegerField()
