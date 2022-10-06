import pytest
from rest_framework.status import HTTP_403_FORBIDDEN

from countries.middleware import CheckCountryByIpMiddleware
from tests.utils.responses import TestHttpResponse


@pytest.mark.django_db
def test_middleware(mocker, add_country_in_black_list):
    request = mocker.MagicMock()

    get_response = TestHttpResponse(status=403)

    request.META = {
        'HTTP_X_FORWARDED_FOR': '109.74.176.0'
    }

    middleware = CheckCountryByIpMiddleware(get_response)
    response = middleware(request)

    assert response.status_code == HTTP_403_FORBIDDEN
