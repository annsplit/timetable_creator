from django.contrib import admin

# Register your models here.
from creator.models import message



class message_admin(admin.ModelAdmin):
    fieldsets = [
        ('Topic',               {'fields': ['topic']}),
        ('Name of scientist', {'fields': ['name']}),
        ('Date', {'fields': ['date']}),
    ]
    list_display = ('topic', 'name', 'date')

admin.site.register(message, message_admin)