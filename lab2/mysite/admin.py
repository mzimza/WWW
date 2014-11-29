from django.contrib import admin

# Register your models here
from models import *


class FreeDateAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['room']}),
        ('Vacancy information', {'fields': ['date', 'From', 'to']}),
    ]
    list_display = ('date', 'room', 'From', 'to')

admin.site.register(FreeDate, FreeDateAdmin)
class ReservationAdmin(admin.ModelAdmin):
	fieldsets = [
		('User', {'fields': ['user']}),
		('Day', {'fields': ['date']}),
		('Room', {'fields': ['room']}),
		('Hours', {'fields': ['From', 'to']}),
	]
	list_display = ('user', 'date', 'From', 'to', 'room')
admin.site.register(Reservation, ReservationAdmin)
class RoomAdmin(admin.ModelAdmin):
	list_display = ('name', 'capacity', 'description')
admin.site.register(Room, RoomAdmin)
admin.site.register(Attribute)



