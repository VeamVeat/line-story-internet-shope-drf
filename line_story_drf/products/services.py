from orders.models import CartItem
from products.models import Product


class ProductServices:
    def __init__(self):
        self.__model = Product

    @staticmethod
    def get_all_product_id_in_cart(user):
        all_product_id_in_cart = list(
            CartItem.objects.get_all_product_in_cart(user).values_list('product__id', flat=True)
        )

        return all_product_id_in_cart

    def get_all_product_photo(self, object_id):
        product = self.__model.objects.get_product(object_id)
        all_photo_product = product.product_file.all()
        return all_photo_product

    def __get_product(self, product_id):
        return self.__model.objects.get(id=product_id)
