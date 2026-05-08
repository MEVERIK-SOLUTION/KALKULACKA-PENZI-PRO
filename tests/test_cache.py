import pytest

from src.backend.cache.redis_cache import RedisCache


@pytest.fixture
def cache():
    c = RedisCache(ttl_seconds=60, prefix="test:")
    c.clear_pattern("test:*")
    yield c
    c.clear_pattern("test:*")


class TestRedisCache:
    def test_set_and_get(self, cache):
        cache.set("key1", "value1")
        val = cache.get("key1")
        assert val == "value1"

    def test_get_missing(self, cache):
        val = cache.get("nonexistent")
        assert val is None

    def test_overwrite(self, cache):
        cache.set("key", "first")
        cache.set("key", "second")
        val = cache.get("key")
        assert val == "second"

    def test_delete(self, cache):
        cache.set("key", "value")
        cache.delete("key")
        val = cache.get("key")
        assert val is None

    def test_clear_pattern(self, cache):
        cache.set("a:1", "data1")
        cache.set("b:1", "data3")
        cache.clear_pattern("test:*")
        assert cache.get("a:1") is None
        assert cache.get("b:1") is None

    def test_ping(self, cache):
        assert cache.ping() is True

    def test_prefix_isolation(self):
        c1 = RedisCache(prefix="ns1:")
        c2 = RedisCache(prefix="ns2:")
        c1.clear_pattern("ns1:*")
        c2.clear_pattern("ns2:*")
        c1.set("shared", "from-ns1")
        c2.set("shared", "from-ns2")
        assert c1.get("shared") == "from-ns1"
        assert c2.get("shared") == "from-ns2"
        c1.delete("shared")
        c2.delete("shared")
