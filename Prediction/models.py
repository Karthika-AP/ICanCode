from django.db import models

# Create your models here.

class Prediction(models.Model):
    opt_title = models.CharField(max_length=140)
    opt_text = models.TextField()
    opt_name = models.CharField(max_length=140)

    def __str__(self):
        return self.opt_title
class Document(models.Model):
    docfile = models.FileField(upload_to='new/')
