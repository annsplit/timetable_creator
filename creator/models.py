from django.db import models

# Create your models here.


class conference(models.Model):
    CName = models.CharField(max_length=200)
    StartDate = models.DateField()
    EndDate = models.DateField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.CName


class time(models.Model):
    Count = models.IntegerField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s" % self.Count


class section(models.Model):
    SName = models.CharField(max_length=200)
    Person = models.CharField(max_length=200, null=True)
    Conference = models.ForeignKey(conference)
    Time = models.ForeignKey(time)
    Date = models.DateTimeField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.SName


class report(models.Model):
    RName = models.CharField(max_length=200)
    Person = models.CharField(max_length=200)
    Sponsor = models.CharField(max_length=200, null=True)
    SID = models.ForeignKey(section)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.RName