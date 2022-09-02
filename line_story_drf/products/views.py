from django.urls import reverse
from django.views.generic import DeleteView
from django_filters import rest_framework as rest_filters
from rest_framework import filters, permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView

from products.filters import ProductFilter
from products.models import ProductFile, Product
from products.serializers import ProductSerializer

# permission на каждую вьюху (заблокирован ли пользователь, ...)


class ProductAPIView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['type__name', 'title']
    ordering_fields = ('title', '-year')
    ordering = ('-year',)


class ProductDetailAPIView(RetrieveAPIView):
    lookup_field = "product_id"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DeleteProductFile(DeleteView):
    model = ProductFile
    permission_required = ['change_profile']

    def get_success_url(self):
        product_id = self.kwargs['product_id']
        return reverse('admin:products_product_change', kwargs={'object_id': product_id})
