from django.db import models
import pyamf 
# Create your models here.

class Content(models.Model):
    contentId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    someValue = models.FloatField()

# pyamf.register_class(Content, 'dugh.flexremoting.Content')
