from django.db import models
from django.db.models import F
from django.shortcuts import get_object_or_404

from products.models import Product
# from products.tasks import send_notification_reserved_product_task
# from orders.tasks import send_purchase_of_goods_notification_task


class OrderServices:
    def __init__(self,
                 user,
                 model=None,
                 product_id=None,
                 object_id=None):
        self.user = user
        self.object_id = object_id
        self.model = model
        self.product_id = product_id

    def order_create(self, total_price_product, total_count_product, product_all, address):
        instance = self.model.objects.create(
                    user=self.user,
                    quantity=total_count_product,
                    final_price=total_price_product,
                    products={'products': product_all},
                    address=address,
                    is_active=True
                )

        # send_purchase_of_goods_notification_task.delay(self.user.email,
        #                                                total_price_product,
        #                                                total_count_product)
        return instance


class CartItemServices:
    def __init__(self,
                 user,
                 model=None,
                 product_id=None,
                 object_id=None):

        self.user = user
        self.object_id = object_id
        self.model = model
        self.product_id = product_id

    def __get_all_cart_item(self):
        return self.model.objects.filter(user=self.user).select_related('product')

    def __get_product_in_cart_by_product_id(self):
        cart_product = get_object_or_404(self.model.objects.select_related('product'),
                                         user=self.user,
                                         product_id=self.product_id)
        return cart_product

    def get_total_price(self):
        cart_item_current_user = self.__get_all_cart_item()
        total_price = cart_item_current_user.aggregate(total_price=models.Sum(F('product__price') * F('quantity')))
        return total_price['total_price']

    def get_total_product_count(self):
        cart_item_current_user = self.__get_all_cart_item()
        total_count = cart_item_current_user.aggregate(total_count=models.Sum(F('quantity')))
        return total_count['total_count']

    def get_quantity_product_in_cart(self):
        product = self.__get_product_in_cart_by_product_id()
        return product.quantity

    def increase_product(self):
        product_success = True

        cart_product = self.__get_product_in_cart_by_product_id()
        product = get_object_or_404(Product, id=self.product_id)

        if not product.is_stock:
            product_success = False
            return product_success

        product.quantity -= 1
        product.save()

        cart_product.quantity += 1
        cart_product.save()

        return product_success

    def diminish_product(self):
        product_success = True

        cart_product = self.__get_product_in_cart_by_product_id()
        product = get_object_or_404(Product, id=self.product_id)

        if cart_product.quantity == 1:
            product_success = False
            return product_success

        product.quantity += 1
        product.save()

        cart_product.quantity -= 1
        cart_product.save()

        return product_success

    def get_products_list(self):
        cart_item_current_user = self.__get_all_cart_item()
        all_products_in_the_dict = [product.product.get_product_in_the_dict for product in cart_item_current_user]
        return all_products_in_the_dict

    def delete_product(self):
        product_in_cart = get_object_or_404(self.model, user=self.user, product_id=self.product_id)
        product = get_object_or_404(Product, id=self.product_id)

        product.quantity += product_in_cart.quantity
        product.save()

        product_in_cart.delete()

    def add_product(self):
        product = get_object_or_404(Product, id=self.product_id)

        cart_item = self.model.objects.create(user=self.user, product_id=product.id)
        product.quantity -= 1
        product.save()

        return cart_item

    def clear(self):
        self.model.objects.filter(user=self.user).delete()


class ReservationServices:
    def __init__(self,
                 user,
                 model=None,
                 product_id=None,
                 count_product=None):

        self.user = user
        self.model = model
        self.product_id = product_id
        self.count_product = count_product

    def make_reservation(self):
        product = get_object_or_404(Product, id=self.product_id)

        object_reservation = self.model(user=self.user,
                                        quantity=self.count_product,
                                        product_id=product.id)

        product.quantity -= self.count_product
        product.save()

        object_reservation.is_reserved = True
        object_reservation.save()

        args_message_notification = (self.user.id,
                                     object_reservation.quantity,
                                     object_reservation.product.price,
                                     object_reservation.product.title,
                                     object_reservation.created_at)

        # send_notification_reserved_product_task.delay(*args_message_notification)
        return object_reservation

    def deleting_reserved_product(self):
        reserved_product = get_object_or_404(self.model, user=self.user, product_id=self.product_id)
        product = get_object_or_404(Product, id=self.product_id)

        product.quantity += reserved_product.quantity
        product.save()

        reserved_product.delete()
