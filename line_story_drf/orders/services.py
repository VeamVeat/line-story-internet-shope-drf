from django.db import models
from django.db.models import F
from django.shortcuts import get_object_or_404

from orders.models import Order, CartItem, Reservation
from products.models import Product


class OrderService:
    def __init__(self):
        self.__model = Order

    def order_create(
            self,
            user,
            total_price_product,
            total_count_product,
            product_all,
            address
    ):
        instance = self.__model.objects.create(
            user=user,
            quantity=total_count_product,
            final_price=total_price_product,
            products={'products': product_all},
            address=address,
            is_active=True
        )
        user.wallet.balance -= total_price_product
        user.save()
        return instance


class CartItemService:
    def __init__(self):
        self.__model = CartItem

    @staticmethod
    def get_total_product_count(cart_item_current_user):
        total_count = list(
            cart_item_current_user.aggregate(
                total_count=models.Sum(F('quantity'))
            ).values())[0]
        return total_count

    @staticmethod
    def get_products_list(all_cart_item_current_user):
        products = [product.product.get_product_in_the_dict
                    for product in all_cart_item_current_user]
        return products

    def check_money_for_make_order(self, user):
        total_price = self.get_total_price(user)
        user_balance = user.wallet.balance

        is_user_money = user_balance > total_price
        return is_user_money

    def get_total_price(self, user):
        cart_item = self.get_all_cart_item(user)
        total_price = list(
            cart_item.aggregate(
                total_price=models.Sum(F('product__price') * F('quantity'))
            ).values()
        )[0]
        return total_price

    def get_quantity_product_in_cart(self, user, product_id):
        product = self.__get_product_in_cart_item_by_product_id(user, product_id)
        return product.quantity

    def increase_product(self, user, product_id):
        """
        :param user: user
        :param product_id: product_id
        :return: product success
        """
        cart_item = self.__get_product_in_cart_item_by_product_id(user, product_id)
        product = get_object_or_404(Product, id=product_id)

        if not product.is_stock:
            return False

        product.quantity -= 1
        product.save()

        cart_item.quantity += 1
        cart_item.save()

        return True

    def diminish_product(self, user, product_id):
        """
        :param user: user
        :param product_id: product_id
        :return: product success
        """
        cart_item = self.__get_product_in_cart_item_by_product_id(user, product_id)
        product = get_object_or_404(Product, id=product_id)

        if cart_item.quantity == 1:
            return False

        product.quantity += 1
        product.save()

        cart_item.quantity -= 1
        cart_item.save()
        return True

    def delete_product(self, user, product_id):
        product_in_cart = get_object_or_404(
            self.__model,
            user=user,
            product_id=product_id
        )
        product = get_object_or_404(Product, id=product_id)

        product.quantity += product_in_cart.quantity
        product.save()

        product_in_cart.delete()

    def add_product(self, user, product_id):
        product = get_object_or_404(Product, id=product_id)

        cart_item = self.__model.objects.create(user=user, product_id=product.id)
        product.quantity -= 1
        product.save()

        return cart_item

    def clear(self, user):
        self.__model.objects.filter(user=user).delete()

    def get_all_cart_item(self, user):
        return self.__model.objects.filter(user=user).select_related('product')

    def __get_product_in_cart_item_by_product_id(self, user, product_id):
        cart_item = get_object_or_404(
            self.__model.objects.select_related('product'),
            user=user,
            product_id=product_id
        )
        return cart_item


class ReservationService:
    def __init__(self, user=None):
        self.__model = Reservation
        self.__user = user

    def make_reservation(self, product_id, quantity):
        product = get_object_or_404(Product, id=product_id)

        object_reservation = self.__model(
            user=self.__user,
            quantity=quantity,
            product_id=product_id
        )

        product.quantity -= quantity
        product.save()

        object_reservation.is_reserved = True
        object_reservation.save()

        return object_reservation

    def deleting_reserved_product(self, product_id):
        reserved_product = get_object_or_404(
            self.__model,
            user=self.__user,
            product_id=product_id
        )
        product = get_object_or_404(Product, id=product_id)

        product.quantity += reserved_product.quantity
        product.save()

        reserved_product.delete()
