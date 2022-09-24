from orders.services import OrderService, CartItemService


class TestOrderService:

    def test_order_create(self, get_client_of_cart_item):
        client, cart_item = get_client_of_cart_item

        cart_item_service = CartItemService()
        cart_item_current_user = cart_item_service.get_all_cart_item(cart_item.user)
        product_all = cart_item_service.get_products_list(cart_item_current_user)
        total_count = cart_item_service.get_total_product_count(cart_item_current_user)
        total_price = cart_item_service.get_total_price(cart_item.user)

        data_from_order_create = {
            'user': cart_item.user,
            'total_price_product': total_price,
            'total_count_product': total_count,
            'product_all': product_all,
            'address': 'Ростовская область'
        }

        order_service = OrderService()
        order = order_service.order_create(**data_from_order_create)

        assert order.user.email == cart_item.user.email
        assert order.quantity == data_from_order_create.get('total_count_product')
        assert order.final_price == data_from_order_create.get('total_price_product')
        assert order.address == data_from_order_create.get('address')
