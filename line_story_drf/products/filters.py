from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter

from products.models import Product


class ProductFilter(rest_filters.FilterSet):

    type = CharFilter(field_name='type__name', lookup_expr='icontains')
    year = NumberFilter(field_name='year', lookup_expr='year')

    class Meta:
        model = Product
        fields = ['type', 'year']