import pytest
from rest_framework.status import HTTP_200_OK

from countries.middleware import CheckCountryByIpMiddleware
from tests.utils.my_responses import MyHttpResponse


@pytest.mark.django_db
def test_middleware(mocker, add_country_in_black_list):
    request = mocker.MagicMock()

    get_response = MyHttpResponse(status=200)

    request.META = {
        'HTTP_X_FORWARDED_FOR': '192.168.1.0'
    }

    middleware = CheckCountryByIpMiddleware(get_response)
    response = middleware(request)

    assert response.status_code == HTTP_200_OK
