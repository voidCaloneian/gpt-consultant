from django.contrib import admin
from .models import Hall, Booking, BookingDetails

admin.site.register(Hall)
admin.site.register(Booking)
admin.site.register(BookingDetails)