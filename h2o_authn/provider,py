import datetime
from typing import Dict
from typing import Optional

import httpx

from h2o_authn import token


class BaseTokenProvider:
    def __init__(
        self,
        *,
        refresh_token: str,
        client_id: str,
        issuer_url: Optional[str] = None,
        token_endpoint_url: Optional[str] = None,
        client_secret: Optional[str] = None,
        scope: Optional[str] = None,
        expiry_threshold: datetime.timedelta = datetime.timedelta(seconds=5),
        expires_in_fallback: datetime.timedelta = datetime.timedelta(seconds=30),
        minimal_expires_in: Optional[datetime.timedelta] = None,
    ) -> None:
        if not token_endpoint_url and not issuer_url:
            raise ValueError(
                "'token_endpoint_url' and 'issuer_url' arguments are mutually exclusive."
                " set only one.",
            )
        if token_endpoint_url and issuer_url:
            raise ValueError(
                "setting 'token_endpoint_url' or 'issuer_url' argument is required."
            )

        self._scope = scope
        self._token_container = token.Container(
            refresh_token=refresh_token,
            expiry_threshold=expiry_threshold,
            expires_in_fallback=expires_in_fallback,
            minimal_expires_in=minimal_expires_in,
            scope=scope,
        )

        self._original_access_token = refresh_token
        self._client_id = client_id
        self._client_secret = client_secret

        if token_endpoint_url:
            self._token_endpoint_url = token_endpoint_url
        if issuer_url:
            self._issuer_url = issuer_url

    def _create_refresh_request_data(self) -> Dict[str, str]:
        data = {
            "grant_type": "refresh_token",
            "client_id": self._client_id,
            "refresh_token": self._token_container.refresh_token,
        }

        if self._client_secret:
            data["client_secret"] = self._client_secret

        if self._scope:
            data["scope"] = self._scope

        return data

    def _fetch_discovery(self, client):
        uri = self._issuer_url.rstrip("/") + "/.well-known/openid-configuration"
        return client.get(uri)

    def _fetch_token(self, client):
        return client.post(
            self._token_endpoint_url,
            data=self._create_refresh_request_data(),
        )

    def _update_token(self, resp: httpx.Response):
        resp_data = resp.json()
        self._token_container.update_token(
            access_token=resp_data["access_token"],
            refresh_token=resp_data.get("refresh_token"),
            expires_in=resp_data.get("expires_in"),
            scope=resp_data.get("scope"),
        )

    def _update_token_endpoint(self, resp: httpx.Response):
        self._token_endpoint_url = resp.json()["token_endpoint"]


class TokenProvider(BaseTokenProvider):
    def __call__(self) -> token.Token:
        self._ensure_token_endpoint_url()
        if self._token_container.refresh_required():
            self._do_refresh()
        return self._token_container.access_token

    def _ensure_token_endpoint_url(self):
        if not self._token_endpoint_url:
            with httpx.Client() as client:
                resp = self._fetch_discovery(client)
            self._update_token_endpoint(resp)

    def _do_refresh(self):
        with httpx.Client() as client:
            resp = self._fetch_token(client)
        self._update_token(resp)


class AsyncTokenProvider(BaseTokenProvider):
    async def __call__(self) -> token.Token:
        await self._ensure_token_endpoint_url()
        if self._token_container.refresh_required():
            await self._do_refresh()
        return self._token_container.access_token

    async def _ensure_token_endpoint_url(self):
        if not self._token_endpoint_url:
            with httpx.Client() as client:
                resp = await self._fetch_discovery(client)
            self._update_token_endpoint(resp)

    async def _do_refresh(self):
        with httpx.Client() as client:
            resp = await self._fetch_token(client)
        self._update_token(resp)
