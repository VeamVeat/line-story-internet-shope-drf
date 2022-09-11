from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from utils.mixins.model_mixins import CreatedAtMixin
from line_story_drf import settings
from orders.managers import CartItemManager, ReservationManager


class Order(CreatedAtMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order')
    slug = models.SlugField(null=True, unique=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('number of products in the order'))
    final_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('total order price')
    )
    products = JSONField()
    address = models.CharField(max_length=1800, verbose_name=_('address'), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('active order'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity of product in the cart'))

    objects = CartItemManager()

    @property
    def get_total_price_product_by_quantity(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('carts items')


class Reservation(CreatedAtMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservation')
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='reservation')
    quantity = models.PositiveIntegerField(default=0, verbose_name=_('quantity of goods reserved'))
    is_reserved = models.BooleanField(default=False)

    objects = ReservationManager()

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')