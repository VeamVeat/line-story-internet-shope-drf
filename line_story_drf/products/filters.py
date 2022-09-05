from django.db.models import Q
from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter

from products.models import Product


class ProductFilter(rest_filters.FilterSet):
    year = NumberFilter(field_name='year', method='filter_year')
    type = CharFilter(field_name='type__name', method='filter_type')

    def filter_year(self, queryset, name, value):
        year_product = self.request.GET.getlist("year")
        queryset = queryset.filter(
            year__in=year_product
        )
        return queryset

    def filter_type(self, queryset, name, value):
        type_product = self.request.GET.getlist("type")

        queryset = queryset.filter(
            type__name__in=type_product
        )
        return queryset

    class Meta:
        model = Product
        fields = {
            'year',
            'type'
        }
