import redis
from django.conf import settings


def get_connect():
    connect_redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    return connect_redis
