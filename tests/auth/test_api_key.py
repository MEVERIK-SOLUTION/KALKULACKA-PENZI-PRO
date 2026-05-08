import importlib
import sys
from pathlib import Path

import pytest
from fastapi import HTTPException
from starlette.requests import Request

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def _reload_auth():
    import src.backend.auth
    importlib.reload(src.backend.auth.api_key)
    return src.backend.auth.api_key


class TestIsValidKey:
    def test_valid_key_from_multi(self, monkeypatch):
        monkeypatch.setenv("API_KEYS", "key1,key2")
        mod = _reload_auth()
        assert mod.is_valid_key("key1") is True
        assert mod.is_valid_key("key2") is True

    def test_invalid_key(self, monkeypatch):
        monkeypatch.setenv("API_KEYS", "key1,key2")
        mod = _reload_auth()
        assert mod.is_valid_key("key3") is False

    def test_null_with_keys_set(self, monkeypatch):
        monkeypatch.setenv("API_KEYS", "key1")
        mod = _reload_auth()
        assert mod.is_valid_key(None) is False

    def test_single_key_env(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "master-key")
        mod = _reload_auth()
        assert mod.is_valid_key("master-key") is True
        assert mod.is_valid_key("wrong") is False

    def test_both_envs_combined(self, monkeypatch):
        monkeypatch.setenv("API_KEYS", "k1,k2")
        monkeypatch.setenv("API_KEY", "k3")
        mod = _reload_auth()
        assert mod.is_valid_key("k1") is True
        assert mod.is_valid_key("k2") is True
        assert mod.is_valid_key("k3") is True
        assert mod.is_valid_key("k4") is False

    def test_no_keys_any_key_accepted(self, monkeypatch):
        monkeypatch.delenv("API_KEYS", raising=False)
        monkeypatch.delenv("API_KEY", raising=False)
        mod = _reload_auth()
        assert mod.is_valid_key(None) is True
        assert mod.is_valid_key("anything") is True


class TestVerifyApiKey:
    def _make_request(self, path: str, api_key: str | None = None) -> Request:
        headers = []
        if api_key:
            headers = [(b"x-api-key", api_key.encode())]
        scope = {"type": "http", "method": "GET", "path": path, "headers": headers}
        return Request(scope)

    async def test_exempt_path_allowed_without_key(self, monkeypatch):
        monkeypatch.setenv("API_KEYS", "secret")
        mod = _reload_auth()
        req = self._make_request("/docs")
        result = await mod.verify_api_key(req)
        assert result is True

    async def test_exempt_path_root(self, monkeypatch):
        monkeypatch.setenv("API_KEYS", "secret")
        mod = _reload_auth()
        req = self._make_request("/")
        result = await mod.verify_api_key(req)
        assert result is True

    async def test_missing_key_returns_401(self, monkeypatch):
        monkeypatch.setenv("API_KEYS", "secret")
        mod = _reload_auth()
        req = self._make_request("/data/inflation")
        with pytest.raises(HTTPException) as exc:
            await mod.verify_api_key(req)
        assert exc.value.status_code == 401

    async def test_invalid_key_returns_403(self, monkeypatch):
        monkeypatch.setenv("API_KEYS", "secret")
        mod = _reload_auth()
        req = self._make_request("/data/inflation", "wrong")
        with pytest.raises(HTTPException) as exc:
            await mod.verify_api_key(req)
        assert exc.value.status_code == 403

    async def test_valid_key_allows_access(self, monkeypatch):
        monkeypatch.setenv("API_KEYS", "secret")
        mod = _reload_auth()
        req = self._make_request("/data/inflation", "secret")
        result = await mod.verify_api_key(req)
        assert result is True

    async def test_no_keys_set_bypasses_auth(self, monkeypatch):
        monkeypatch.delenv("API_KEYS", raising=False)
        monkeypatch.delenv("API_KEY", raising=False)
        mod = _reload_auth()
        req = self._make_request("/data/inflation")
        result = await mod.verify_api_key(req)
        assert result is True
