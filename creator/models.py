from django.db import models
from django import forms

# Create your models here.

class conference(models.Model):
    CName = models.CharField(max_length=200)
    StartDate = models.DateField()
    EndDate = models.DateField()
    DayStart = models.TimeField(default="9:00")
    DayEnd = models.TimeField(default="20:00")
    plenary = models.IntegerField(default=25)
    p_questions = models.IntegerField(default=5)
    sectional = models.IntegerField(default=15)
    s_questions = models.IntegerField(default=5)
    database = models.CharField(max_length=200, default="agora")
    authors_table = models.CharField(max_length=200)
    reports_table = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s" % self.CName


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
    Conference = models.ForeignKey(conference)
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"%s" % self.TName





class section(models.Model):
    SName = models.CharField(max_length=200)
    Person = models.CharField(max_length=200, null=True, blank=True)
    Conference = models.ForeignKey(conference)
    Place = models.CharField(max_length=200)
    Type = models.ForeignKey(section_type)
    StartTime = models.DateTimeField(blank=True, null=True)
    x_pos = models.FloatField(default=0)
    y_pos = models.FloatField(default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        from datetime import datetime
        param = "%Y-%m-%d %H:%M"
        return u"%s, %s" % (self.SName, datetime.strftime(self.StartTime, param))


class report(models.Model):
    rid = models.IntegerField()
    RName = models.CharField(max_length=200)
    Annotation = models.TextField()
    Reporter = models.CharField(max_length=200)
    Topic = models.CharField(max_length=200)
    Session = models.CharField(max_length=200)
    Organisation = models.CharField(max_length=200)
    Author = models.CharField(max_length=200)
    Sponsor = models.CharField(max_length=200, blank=True)
    IsFinal = models.BooleanField()
    Conference = models.ForeignKey(conference)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s" % self.RName


class event(models.Model):
    order = models.IntegerField(default=0)
    x_pos = models.FloatField(default=0)
    y_pos = models.FloatField(default=0)
    Section = models.ForeignKey(section, null=True, blank=True, on_delete=models.SET_NULL)
    Report = models.OneToOneField(report, null=True, blank=True,on_delete=models.SET_NULL)
    Conference = models.ForeignKey(conference)
    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s" % self.Report


