from django.contrib import admin

from .models import Flight,Airport,Passenger

# Register your models here.

class FlightAdmin(admin.ModelAdmin):
    list_display = ("origin","destination","duration")

class AirportAdmin(admin.ModelAdmin):
    list_display = ("code","city")


class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)
    list_display = ("first","last")

admin.site.register(Airport,AirportAdmin)
admin.site.register(Flight,FlightAdmin)
admin.site.register(Passenger,PassengerAdmin)