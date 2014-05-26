# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from creator.models import report, conference, section, section_type, event



class report_admin(admin.ModelAdmin):
    fieldsets = [
        (u'ID доклада в системе "Агора"',       {'fields': ['rid']}),
        (u'Конференция',                        {'fields': ['Conference']}),
        (u'Название',                           {'fields': ['RName']}),
        (u'Аннотация',                          {'fields': ['Annotation']}),
        (u'Докладчик',                          {'fields': ['Reporter']}),
        (u'Тематика',                           {'fields': ['Topic']}),
        (u'Сессия',                             {'fields': ['Session']}),
        (u'Организация',                        {'fields': ['Organisation']}),
        (u'Авторы',                             {'fields': ['Author']}),
        (u'Спорсор',                            {'fields': ['Sponsor']}),
        (u'Получена финальная версия статьи',   {'fields': ['IsFinal']}),
    ]
    list_display = ('RName', 'Conference', 'Topic', 'Author', 'Sponsor', 'Session')
    list_filter = ['Conference', 'Topic', 'Session', 'Sponsor', 'IsFinal']
    ordering = ['-Conference', 'Topic', 'Session', 'RName']
    search_fields = ['RName', 'Annotation', 'Author', 'Sponsor', 'Reporter', 'Organisation']


class conference_admin(admin.ModelAdmin):
    readonly_fields=('id',)
    fieldsets = [
        (u'ID конференции',                         {'fields': ['id']}),
        (u'Название',                               {'fields': ['CName']}),
        (u'Дата начала',                            {'fields': ['StartDate']}),
        (u'Дата окончания',                         {'fields': ['EndDate']}),
        (u'Начало дня',                             {'fields': ['DayStart']}),
        (u'Конец дня',                              {'fields': ['DayEnd']}),
        (u'Продолжительность пленарных докладов',   {'fields': ['plenary']}),
        (u'Время на вопросы к пленарным докладам',  {'fields': ['p_questions']}),
        (u'Продолжительность секционных докладов',  {'fields': ['sectional']}),
        (u'Время на вопросы к пленарным докладам',  {'fields': ['s_questions']}),
        (u'Название базы данных в системе "Агора"', {'fields': ['database']}),
        (u'Название таблицы с данными об авторах',  {'fields': ['authors_table']}),
        (u'Название таблицы с данными о докладах',  {'fields': ['reports_table']}),
        (u'Логин для доступа к БД "Агора"',         {'fields': ['login']}),
        (u'Пароль для доступа к БД "Агора"',        {'fields': ['password']}),
    ]
    list_display = ('CName', 'StartDate', 'EndDate')


class section_admin(admin.ModelAdmin):
    fieldsets = [
        (u'Название',                                                   {'fields': ['SName']}),
        (u'Председатель',                                               {'fields': ['Person']}),
        (u'Дата и время начала',                                        {'fields': ['StartTime']}),
        (u'Конференция',                                                {'fields': ['Conference']}),
        (u'Место проведения',                                           {'fields': ['Place']}),
        (u'Тип',                                                        {'fields': ['Type']}),
        (u'Ширина блока в расписании (0 - по умолчанию типа секции)',   {'fields': ['x_pos']}),
        (u'Высота блока в расписании (0 - по умолчанию типа секции)',   {'fields': ['y_pos']}),
    ]
    list_display = ('StartTime', 'SName', 'Person', 'Place', 'Conference')
    list_display_links = ['SName']
    list_filter = ('Conference', 'Type')
    ordering = ['-Conference', 'StartTime', 'SName']


class section_type_admin(admin.ModelAdmin):
    fieldsets = [
        (u'Тип',                            {'fields': ['TName']}),
        (u'Цвет секций в расписании',       {'fields': ['color']}),
        (u'Продолжительность по умолчанию', {'fields': ['time_default']}),
        (u'Конференция',                    {'fields': ['Conference']})

    ]
    list_display = ('TName', 'color', 'Conference')
    list_filter = ('Conference', 'TName', 'color')
    ordering = ['-Conference', 'TName']


class event_admin(admin.ModelAdmin):
    fieldsets = [
        (u'Конференция',                                    {'fields': ['Conference']}),
        (u'Секция',                                         {'fields': ['Section']}),
        (u'Номер по порядку в секции',                      {'fields': ['order']}),
        (u'Ширина блока в расписании (0 - по умолчанию)',   {'fields': ['x_pos']}),
        (u'Ширина блока в расписании (0 - по умолчанию)',   {'fields': ['y_pos']}),
        (u'Связанный доклад',                               {'fields': ['Report']})
    ]
    list_display = ('Report', 'Conference', 'Section', 'order')
    list_filter = ['Conference']
    ordering = ['-Conference', 'Report__RName']


admin.site.register(report, report_admin)
admin.site.register(conference, conference_admin)
admin.site.register(section, section_admin)
admin.site.register(section_type, section_type_admin)
admin.site.register(event, event_admin)
