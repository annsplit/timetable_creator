# -*- coding: utf-8 -*-

from django.db import models
from django import forms

# Create your models here.

class conference(models.Model):
    CName = models.CharField(u"Название", max_length=200)
    StartDate = models.DateField(u"Дата начала")
    EndDate = models.DateField(u"Дата окончания")
    DayStart = models.TimeField(u"Начало дня", default="9:00")
    DayEnd = models.TimeField(u"Конец дня", default="20:00")
    plenary = models.IntegerField(u"(в минутах)", default=25)
    p_questions = models.IntegerField(u"(в минутах)",default=5)
    sectional = models.IntegerField(u"(в минутах)",default=15)
    s_questions = models.IntegerField(u"(в минутах)",default=5)
    database = models.CharField(u"База данных", max_length=200, default="agora")
    authors_table = models.CharField(u"Таблица авторов", max_length=200)
    reports_table = models.CharField(u"Таблица докладов", max_length=200)
    login = models.CharField(u"Логин", max_length=200)
    password = models.CharField(u"Пароль", max_length=200)
    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s" % self.CName
    class Meta:
        verbose_name = u"конференцию"
        verbose_name_plural = u"Конференции"


class section_type(models.Model):
    COLOR_CHOICES = (
        ('white', u"Белый"),
        ('mediumpurple', u'Фиолетовый'),
        ('greenyellow', u'Зеленый'),
        ('#FF0000', u'Красный'),
        ('ghostwhite', u'Светло-серый'),
        ('#F3F781', u'Светло-желтый'),
        ('#58ACFA', u'Голубой'),
        ('#F6D8CE', u'Розовый'),
        ('#CEF6D8', u'Светло-зеленый'),
        ('#F3E2A9', u'Оранжевый'),
    )
    TName = models.CharField(u"Название", max_length=200)
    color = models.CharField(u"Цвет", max_length=40, choices=COLOR_CHOICES)
    time_default = models.IntegerField(u"(в минутах)")
    Conference = models.ForeignKey(conference, verbose_name=u"Конференция")
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"%s" % self.TName
    class Meta:
        verbose_name = u"тип секции"
        verbose_name_plural = u"Типы секций"




class section(models.Model):
    SName = models.CharField(u"Название", max_length=200)
    Person = models.CharField(u"Председатель", max_length=200, null=True, blank=True)
    Conference = models.ForeignKey(conference, verbose_name=u"Конференция")
    Place = models.CharField(u"Место проведения", max_length=200)
    Type = models.ForeignKey(section_type, verbose_name=u"Тип секции")
    StartTime = models.DateTimeField(u"Дата и время начала", blank=True, null=True)
    x_pos = models.FloatField(u"Ширина", default=0)
    y_pos = models.FloatField(u"Высота",default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        from datetime import datetime
        param = "%Y-%m-%d %H:%M"
        return u"%s" % self.SName
    class Meta:
        verbose_name = u"секцию"
        verbose_name_plural = u"Секции"

class report(models.Model):
    rid = models.IntegerField(u"ID доклада в системе Агора")
    RName = models.CharField(u"Название", max_length=200)
    Annotation = models.TextField(u"Аннотация")
    Reporter = models.CharField(u"Докладчик", max_length=200)
    Topic = models.CharField(u"Тематика", max_length=200)
    Session = models.CharField(u"Сессия", max_length=200)
    Organisation = models.CharField(u"Организация", max_length=200)
    Author = models.CharField(u"Авторы", max_length=200)
    Sponsor = models.CharField(u"Спонсор", max_length=200, blank=True)
    IsFinal = models.BooleanField(u"Получена финальная версия статьи")
    Conference = models.ForeignKey(conference, verbose_name=u"Конференция")
    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s" % self.RName
    class Meta:
        verbose_name = u"доклад"
        verbose_name_plural = u"Доклады"


class event(models.Model):
    order = models.IntegerField(u"Номер", default=0)
    x_pos = models.FloatField(u"Ширина", default=0)
    y_pos = models.FloatField(u"Высота", default=0)
    Section = models.ForeignKey(section, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=u"Секция")
    Report = models.OneToOneField(report, null=True, blank=True,on_delete=models.SET_NULL, verbose_name=u"Доклад")
    Conference = models.ForeignKey(conference, verbose_name=u"Конференция")
    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s" % self.Report
    class Meta:
        verbose_name = u"событие"
        verbose_name_plural = u"События"


