from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import DeleteView
from rest_framework.generics import get_object_or_404, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from products.models import ProductFile, Product
from products.serializers import ProductSerializer


class ProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# class ProductDetailAPIView(APIView):
#     serializer_class = ProductSerializer
#
#     @staticmethod
#     def get_queryset():
#         products = Product.objects.all()
#         return products
#
#     def get(self, request, *args, **kwargs):
#         product_id = kwargs.get('pk')
#         product = get_object_or_404(Product, id=product_id)
#
#         product_serializer = ProductSerializer(data=product)
#         if product_serializer.is_valid():
#             product_serializer.save()
#             return JsonResponse(product_serializer.data, status=201)
#         return JsonResponse(product_serializer.data, status=400)

class ProductDetailAPIView(RetrieveAPIView):
    lookup_field = "id"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DeleteProductFile(DeleteView):
    model = ProductFile
    permission_required = ['change_profile']

    def get_success_url(self):
        product_id = self.kwargs['product_id']
        return reverse('admin:products_product_change', kwargs={'object_id': product_id})