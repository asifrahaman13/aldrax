import hashlib


class RedisRepository:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.timeout = 300

    def get_cached_key(self, query: str) -> str:
        return hashlib.md5(query.encode()).hexdigest()

    def get_cached_data(self, cache_key: str):
        return self.redis_client.get(cache_key)

    def set_cache_data(self, cache_key: str, value: str):
        return self.redis_client.setex(cache_key, self.timeout, value)
