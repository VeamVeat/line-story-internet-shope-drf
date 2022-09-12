from django.utils.encoding import smart_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.generics import get_object_or_404

from users.models import User


class Uid64Service:

    @staticmethod
    def get_uid64_by_user_id(user_id):
        return urlsafe_base64_encode(smart_bytes(user_id))

    @staticmethod
    def get_user_by_uid64(uid64):
        user_id = force_str(urlsafe_base64_decode(uid64))
        user = get_object_or_404(User, id=user_id)
        return user
