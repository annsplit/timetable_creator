from django.contrib import admin

# Register your models here.
from creator.models import report, conference, section, section_type, event, reports_time



class report_admin(admin.ModelAdmin):
    fieldsets = [
        ('Name',               {'fields': ['RName']}),
        ('Annotation',   {'fields': ['Annotation']}),
        ('Reporter',              {'fields': ['Reporter']}),
        ('Topic',              {'fields': ['Topic']}),
        ('Session',              {'fields': ['Session']}),
        ('Organisation',              {'fields': ['Organisation']}),
        ('Author',              {'fields': ['Author']}),
        ('Sponsor',              {'fields': ['Sponsor']}),
        ('IsFinal',              {'fields': ['IsFinal']}),
    ]
    list_display = ('RName', 'Reporter', 'Sponsor', 'Session')


class conference_admin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['CName']}),
        ('Start date', {'fields': ['StartDate']}),
        ('End date', {'fields': ['EndDate']}),
        ('daystart', {'fields': ['DayStart']}),
        ('dayend', {'fields': ['DayEnd']}),
        ('RepTime', {'fields': ['RepTime']})
    ]
    list_display = ('CName', 'StartDate', 'EndDate')


class section_admin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['SName']}),
        ('Person', {'fields': ['Person']}),
        ('StartDateTime', {'fields': ['StartTime']}),
        ('Conference', {'fields': ['Conference']}),
        ('Place', {'fields': ['Place']}),
        ('Type', {'fields': ['Type']}),
        ('x', {'fields': ['x_pos']}),
        ('y', {'fields': ['y_pos']}),
    ]
    list_display = ('SName', 'Person', 'StartTime', 'Place', 'Conference')


class section_type_admin(admin.ModelAdmin):
    fieldsets = [
        ('Type', {'fields': ['TName']}),
        ('color', {'fields': ['color']}),
        ('time_default', {'fields': ['time_default']})

    ]
    list_display = ('TName', 'color')


class event_admin(admin.ModelAdmin):
    fieldsets = [
        ('Conference', {'fields': ['Conference']}),
        ('Section', {'fields': ['Section']}),
        ('order', {'fields': ['order']}),
        ('x', {'fields': ['x_pos']}),
        ('y', {'fields': ['y_pos']}),
        ('Report', {'fields': ['Report']})
    ]
    list_display = ('Report', 'Conference', 'Section', 'order')


class reports_time_admin(admin.ModelAdmin):
    fieldsets = [
        ('plenary', {'fields': ['plenary']}),
        ('sectional', {'fields': ['sectional']})
    ]
    list_display = ('plenary', 'sectional')

admin.site.register(reports_time, reports_time_admin)
admin.site.register(report, report_admin)
admin.site.register(conference, conference_admin)
admin.site.register(section, section_admin)
admin.site.register(section_type, section_type_admin)
admin.site.register(event, event_admin)
