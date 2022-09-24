from django.contrib import admin

from countries.models import Country, BlacklistedCountry


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'reduction')


@admin.register(BlacklistedCountry)
class BlacklistedCountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'country')
