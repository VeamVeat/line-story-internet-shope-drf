import logging

from geoip import geolite2
from django.http import HttpResponseForbidden

from countries.models import BlacklistedCountry


class CheckCountryByIpMiddleware:
    def __init__(self, get_response):
        self.__get_response = get_response
        self.__logger = logging.getLogger(__name__)

    @staticmethod
    def __get_ip_by_request(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        elif request.META.get('HTTP_X_REAL_IP'):
            ip = request.META.get('HTTP_X_REAL_IP')
        else:
            ip = request.META.get('REMOTE_ADDR')
        return str(ip)

    @staticmethod
    def __is_black_list_country(country_name):
        return BlacklistedCountry.objects.filter(country__reduction=country_name).exists()

    def __call__(self, request):
        user_ip = self.__get_ip_by_request(request)
        ip_info = geolite2.lookup(user_ip)

        if ip_info is None:
            request.META['USER_COUNTRY'] = 'None'
            self.__logger.info('Country not recognized')
            return self.__get_response(request)

        country = ip_info.country

        if self.__is_black_list_country(country):
            return HttpResponseForbidden("This country is blocked by the administrator", 403)

        request.META['USER_COUNTRY'] = country

        return self.__get_response(request)
