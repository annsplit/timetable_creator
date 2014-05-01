from django.contrib import admin

# Register your models here.
from creator.models import report, conference, section, time



class report_admin(admin.ModelAdmin):
    fieldsets = [
        ('Topic',               {'fields': ['RName']}),
        ('Name of scientist',   {'fields': ['Person']}),
        ('Person',              {'fields': ['Sponsor']}),
        ('Section',              {'fields': ['SID']}),
    ]
    list_display = ('RName', 'Person', 'Sponsor')


class conference_admin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['CName']}),
        ('Start date', {'fields': ['StartDate']}),
        ('End date', {'fields': ['EndDate']})
    ]


class section_admin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['SName']}),
        ('Person', {'fields': ['Person']}),
        ('date', {'fields': ['Date']}),
        ('StartTime', {'fields': ['StartTime']}),
        ('Conference', {'fields': ['Conference']}),
        ('TimeCount', {'fields': ['TimeCount']})
    ]


class time_admin(admin.ModelAdmin):
    fieldsets = [
        ('Count', {'fields': ['Count']})
    ]

admin.site.register(report, report_admin)
admin.site.register(conference, conference_admin)
admin.site.register(section, section_admin)
admin.site.register(time, time_admin)