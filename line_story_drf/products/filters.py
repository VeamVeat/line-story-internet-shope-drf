from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter

from products.models import Product


class ProductFilter(rest_filters.FilterSet):
    year = NumberFilter(field_name='year', method='filter_year')
    type = CharFilter(field_name='type__name', method='filter_type')

    def filter_year(self, queryset, name, value):
        queryset = queryset.filter(
            year__in=value
        )
        return queryset

    def filter_type(self, queryset, name, value):
        queryset = queryset.filter(
            type__name__in=value
        )
        return queryset

    class Meta:
        model = Product
        fields = {
            'year',
            'type'
        }
