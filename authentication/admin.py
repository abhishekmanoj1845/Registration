from .models import Deparments
from .models import doctors
from django.contrib import admin
from .models import Booking

# Register your models here.

admin.site.register(Deparments)
admin.site.register(doctors)
class BookingAdmin(admin.ModelAdmin):
    list_display=('id','p_name','p_phone','p_email','doc_name','booking_date','booked_on')


admin.site.register(Booking,BookingAdmin)