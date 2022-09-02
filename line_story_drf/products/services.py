from orders.models import CartItem


class ProductServices:
    def __init__(self,
                 user,
                 model,
                 product_id=None,
                 object_id=None):
        self.user = user
        self.object_id = object_id
        self.model = model
        self.product_id = product_id

    def get_all_product_id_in_cart(self):
        all_product_in_cart = CartItem.objects.get_all_product_in_cart(self.user)
        all_product_id_in_cart = [product_in_cart.product.id
                                  for product_in_cart in all_product_in_cart]
        return all_product_id_in_cart

    def get_all_product_photo(self):
        current_product = self.model.objects.get_product_files(self.object_id)
        all_photo_product = current_product.product_file.all()
        return all_photo_product

    def get_product(self):
        return self.model.objects.get(id=self.product_id)
