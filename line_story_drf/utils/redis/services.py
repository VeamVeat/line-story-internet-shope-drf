from django.conf import settings

import redis


class RedisService:
    def __init__(self, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB):
        self.__connect_redis = redis.StrictRedis(host, port, db, decode_responses=True)
        self.__type_dict = {
            'int': int,
            'str': str
        }

    def get(self, key, val_type='int'):
        value = self.__connect_redis.get(key)

        if value is None:
            return None

        value_type = self.__type_dict.get(val_type)
        return value_type(value)

    def set(self, key, value, val_type='str'):
        value_type = self.__type_dict.get(val_type)
        self.__connect_redis.set(value_type(key), value_type(value))

    def delete(self, key):
        """
        :param key: key
        :return: 1 if successful else 0
        """
        return self.__connect_redis.delete(key)
