from orders.models import Reservation
from orders.services import ReservationService
from tests.settings import TEST_QUANTITY_IN_RESERVED, TEST_QUANTITY_PRODUCT


class TestReservationService:

    @staticmethod
    def __is_product_reserved_by_user(reserved_product):
        reserved_product_exist = Reservation.objects.filter(
            user=reserved_product.user,
            product_id=reserved_product.product.id
        ).exists()

        return reserved_product_exist

    def test_make_reservation(self, create_user, create_product):
        user = create_user
        product = create_product

        reservation_service = ReservationService(user)
        object_reservation = reservation_service.make_reservation(
            product_id=product.id,
            quantity=TEST_QUANTITY_IN_RESERVED
        )
        product.refresh_from_db()

        assert product.quantity == (TEST_QUANTITY_PRODUCT - TEST_QUANTITY_IN_RESERVED)
        assert object_reservation.quantity == TEST_QUANTITY_IN_RESERVED
        assert object_reservation.product.id == product.id

    def test_deleting_reserved_product(self, get_client_of_reserved_product):
        client, reserved_product = get_client_of_reserved_product

        reservation_service = ReservationService(reserved_product.user)
        reservation_service.deleting_reserved_product(product_id=reserved_product.product.id)

        is_product_reserved = self.__is_product_reserved_by_user(reserved_product)

        assert not is_product_reserved
