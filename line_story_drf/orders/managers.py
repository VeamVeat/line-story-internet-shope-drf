from django.db import models


class CartItemManager(models.Manager):
    def get_all_product_in_cart(self, user):
        return self.filter(user=user).select_related('product')


class ReservationManager(models.Manager):
    def get_all_reservation_product(self, user):
        return self.filter(user=user).select_related('product')