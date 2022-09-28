from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('country'))
    reduction = models.CharField(max_length=255, verbose_name=_('reduction'), null=True, blank=True)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return f'Country {self.name}'


class BlacklistedCountry(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='country')

    class Meta:
        verbose_name = _('country in black list')
        verbose_name_plural = _('countries in black list')

    def __str__(self):
        return f'Country {self.country.name} is blocked'
