from django.contrib import admin

from rentals.models import Rental

# Register your models here.
admin.site.register([
    Rental
])