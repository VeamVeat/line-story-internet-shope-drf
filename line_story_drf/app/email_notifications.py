import logging

from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model()

logger = logging.getLogger(__name__)


def send_notification_new_product(product_title, product_price):

    title_message = 'New product'
    html_page = 'products/new_product_notification.html'
    all_user = User.objects.all()

    for user in all_user:
        message = render_to_string(
            html_page,
            {
                'user': user,
                'product_title': product_title,
                'product_price': product_price
            }
        )
        user.email_user(title_message, message)


def send_notification_reserved_product(
        user_id,
        reserved_product_count,
        product_price,
        product_title,
        time_reserved
):

    title_message = 'Reservation product'
    html_page = 'orders/new_reserved_notification.html'
    user = get_object_or_404(User, id=user_id)

    message = render_to_string(
        html_page,
        {
            'user': user,
            'product_count': reserved_product_count,
            'product_title': product_title,
            'product_price': product_price,
            'time_reserved': time_reserved
        }
    )
    user.email_user(title_message, message)


def send_purchase_of_goods_notification(email, total_price, total_count):

    title_message = 'Your order has been completed'
    html_page = 'orders/new_order_notification.html'
    user = get_object_or_404(User, email=email)

    message = render_to_string(
        html_page,
        {
            'user': user,
            'total_price': total_price,
            'total_count': total_count
        }
    )
    user.email_user(title_message, message)
