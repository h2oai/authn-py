import datetime
from typing import Dict
from typing import Optional

import httpx

__version__ = "0.0.0"


class Token(str):
    exp: datetime.datetime
    scope: Optional[str]

    def __new__(cls, value: str, exp: datetime.datetime, scope: str):
        token = str(value)
        setattr(token, "exp", exp)
        setattr(token, "scope", scope)
        return token


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
        expiry_threshold_band: datetime.timedelta = datetime.timedelta(seconds=5),
        fallback_expires_in: datetime.timedelta = datetime.timedelta(seconds=30),
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

        self._refresh_token = refresh_token
        self._original_access_token = refresh_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._expiry_threshold_band = expiry_threshold_band
        self._fall_back_token_expires_in = fallback_expires_in
        self._minimal_expires_in = minimal_expires_in
        self._scope = scope

        if token_endpoint_url:
            self._token_endpoint_url = token_endpoint_url
        if issuer_url:
            self._issuer_url = issuer_url

        self._access_token: Optional[Token] = None
        self._access_token_exp: Optional[datetime.datetime] = None

    def _refresh_required(self) -> bool:
        if self._access_token is None or self._access_token_exp is None:
            return True

        now = datetime.datetime.now(datetime.timezone.utc)
        return self._access_token_exp <= (now + self._expiry_threshold_band)

    def _create_refresh_request_data(self) -> Dict[str, str]:
        data = {
            "grant_type": "refresh_token",
            "client_id": self._client_id,
            "refresh_token": self._refresh_token,
        }

        if self._client_secret:
            data["client_secret"] = self._client_secret

        if self._scope:
            data["scope"] = self._scope

        return data

    def _set_access_token(self, resp: httpx.Response):
        resp_data = resp.json()

        access_token: str = resp_data["access_token"]
        expires_in: int = resp_data.get("expires_in")

        exp_delta = self._fall_back_token_expires_in
        if expires_in:
            exp_delta = datetime.timedelta(seconds=expires_in)

        now = datetime.datetime.now(datetime.timezone.utc)
        exp = now + exp_delta
        scope = resp_data.get("scope", self._scope)

        refresh_token = resp_data("refresh_token")
        if refresh_token:
            self._refresh_token = refresh_token

        self._access_token = Token(access_token, exp=exp, scope=scope)
        self._access_token_exp = exp
        if self._minimal_expires_in:
            self._access_token_exp = min(exp, now + self._minimal_expires_in)

    # Awaitable


class TokenProvider(BaseTokenProvider):
    def __call__(self) -> Token:
        self._ensure_token_endpoint_url()
        if self._refresh_required():
            self._do_refresh()
        if not self._access_token:
            raise LookupError("Could not obtain access token")
        return self._access_token

    def _ensure_token_endpoint_url(self) -> str:
        if not self._token_endpoint_url:
            uri = self._issuer_url.rstrip("/") + "/.well-known/openid-configuration"
            with httpx.Client() as client:
                resp = client.get(uri)
            self._token_endpoint_url = _extract_token_endpoint(resp)
        return self._token_endpoint_url

    def _do_refresh(self):
        with httpx.Client() as client:
            resp = client.post(
                self._token_endpoint_url,
                data=self._create_refresh_request_data(),
            )
        self._set_access_token(resp)


class AsyncTokenProvider(BaseTokenProvider):
    async def __call__(self) -> Token:
        await self._ensure_token_endpoint_url()
        if self._refresh_required():
            await self._do_refresh()
        if not self._access_token:
            raise LookupError("Could not obtain access token")
        return self._access_token

    async def _ensure_token_endpoint_url(self) -> str:
        if not self._token_endpoint_url:
            uri = self._issuer_url.rstrip("/") + "/.well-known/openid-configuration"
            async with httpx.AsyncClient() as client:
                resp = await client.get(uri)
            self._token_endpoint_url = _extract_token_endpoint(resp)
        return self._token_endpoint_url

    async def _do_refresh(self):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self._token_endpoint_url,
                data=self._create_refresh_request_data(),
            )
        self._set_access_token(resp)


def _extract_token_endpoint(response: httpx.Response) -> str:
    return response.json()["token_endpoint"]
