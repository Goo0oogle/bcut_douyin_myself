# coding: utf-8
from hashlib import md5

from redis_helper import redis_cli


def get_md5(text):
    if isinstance(text, str):
        text = text.encode('utf-8')
    return md5(text).hexdigest()


class SetDuplicate:
    redis = redis_cli

    def __init__(self, redis_key="local_zset_duplicate"):
        self.redis_key = redis_key

    def pre_text(self, text, use_hash=True):
        if not isinstance(text, str):
            text = str(text)
        return get_md5(text.encode()) if use_hash else text

    def contains(self, value, redis_key=None):
        redis_key = redis_key or self.redis_key
        md5_value = get_md5(value)
        return self.redis.sismember(redis_key, md5_value)

    def insert(self, text, redis_key=None, use_hash=True):
        text = self.pre_text(text, use_hash)
        redis_key = redis_key or self.redis_key
        result = self.redis.sadd(redis_key, text)
        return bool(result)
