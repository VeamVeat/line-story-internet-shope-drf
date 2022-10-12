import logging

from line_story_drf.celery import app
from app.email_notifications import send_purchase_of_goods_notification, cart_clear

logger = logging.getLogger(__name__)


@app.task(name="send_notification_new_order_product")
def send_purchase_of_goods_notification_task(*args):
    logger.info("Sent notification_reserved_product")
    return send_purchase_of_goods_notification(*args)


@app.task(name="send_notification_cart_clear")
def cart_clear_task(*args):
    logger.info("Sent notification_reserved_product")
    return cart_clear(*args)
