from django.db import models
from django import forms

# Create your models here.

class reports_time(models.Model):
    plenary = models.IntegerField()
    sectional = models.IntegerField()



class conference(models.Model):
    CName = models.CharField(max_length=200)
    StartDate = models.DateField()
    EndDate = models.DateField()
    DayStart = models.TimeField()
    DayEnd = models.TimeField()
    RepTime = models.OneToOneField(reports_time)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.CName


class section_type(models.Model):
    COLOR_CHOICES = (
        ('white', 'White'),
        ('mediumpurple', 'Purple'),
        ('greenyellow', 'Green'),
        ('#FF0000', 'Red'),
        ('ghostwhite', 'Light gray'),
        ('#F3F781', 'Light yellow'),
        ('#58ACFA', 'Light blue'),
        ('#F6D8CE', 'Light pink'),
        ('#CEF6D8', 'Light green'),
        ('#F3E2A9', 'Light orange'),
    )
    TName = models.CharField(max_length=200)
    color = models.CharField(max_length=40, choices=COLOR_CHOICES)
    time_default = models.IntegerField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.TName





class section(models.Model):
    SName = models.CharField(max_length=200)
    Person = models.CharField(max_length=200, null=True, blank=True)
    Conference = models.ForeignKey(conference)
    Place = models.CharField(max_length=200)
    Type = models.ForeignKey(section_type)
    #TimeCount = models.ForeignKey(time)
    StartTime = models.DateTimeField(blank=True, null=True)
    x_pos = models.FloatField(default=0)
    y_pos = models.FloatField(default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.SName


class report(models.Model):
    rid = models.IntegerField()
    RName = models.CharField(max_length=200)
    Annotation = models.CharField(max_length=200)
    Reporter = models.CharField(max_length=200)
    Topic = models.CharField(max_length=200)
    Session = models.CharField(max_length=200)
    Organisation = models.CharField(max_length=200)
    Author = models.CharField(max_length=200)
    Sponsor = models.CharField(max_length=200, blank=True)
    IsFinal = models.BooleanField()

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.RName


class event(models.Model):
    order = models.IntegerField(null=True, blank=True)
    x_pos = models.FloatField(default=0)
    y_pos = models.FloatField(default=0)
    Section = models.ForeignKey(section, null=True, blank=True)
    Report = models.OneToOneField(report, null=True, blank=True,on_delete=models.SET_NULL,)
    Conference = models.ForeignKey(conference)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.Report


