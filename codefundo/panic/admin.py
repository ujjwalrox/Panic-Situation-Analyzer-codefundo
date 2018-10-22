from django.contrib import admin

from .models import Location, Account, PanicLocation

# Register your models here.

admin.site.register(Location)
admin.site.register(Account)
admin.site.register(PanicLocation)
