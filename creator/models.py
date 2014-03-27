from django.db import models

# Create your models here.
class message(models.Model):
    topic = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    date = models.DateTimeField('date')
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.topic