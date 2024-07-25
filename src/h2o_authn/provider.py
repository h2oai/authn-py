import datetime
import ssl
from typing import Dict
from typing import Optional

import httpx

from h2o_authn import error
from h2o_authn import token

DEFAULT_EXPIRY_THRESHOLD = datetime.timedelta(seconds=5)
DEFAULT_EXPIRES_IN_FALLBACK = datetime.timedelta(seconds=30)

DEFAULT_HTTP_TIMEOUT = datetime.timedelta(seconds=5)


class _BaseTokenProvider:
    def __init__(
        self,
        *,
        refresh_token: str,
        client_id: str,
        issuer_url: Optional[str] = None,
        token_endpoint_url: Optional[str] = None,
        client_secret: Optional[str] = None,
        scope: Optional[str] = None,
        expiry_threshold: datetime.timedelta = DEFAULT_EXPIRY_THRESHOLD,
        expires_in_fallback: datetime.timedelta = DEFAULT_EXPIRES_IN_FALLBACK,
        http_timeout: datetime.timedelta = DEFAULT_HTTP_TIMEOUT,
        minimal_refresh_period: Optional[datetime.timedelta] = None,
        http_ssl_context: Optional[ssl.SSLContext] = None,
    ) -> None:
        """Returns a new instance of the token provider.

        Args:
            refresh_token: Refresh token which will used for the access token exchange.
            client_id: OAuth 2.0 client id that will be used or the access token
                exchange.
            issuer_url: Base URL of the issuer. This URL will be used for the discovery
                to obtain token endpoint. Mutually exclusive with the
                token_endpoint_url argument.
            token_endpoint_url: URL of the token endpoint that should be used for the
                access token exchange. Mutually exclusive with the issuer_url argument.
            client_secret: Optional OAuth 2.0 client secret for the confidential
                clients. Used only when provided.
            scope: Optionally sets the the scope for which the access token should be
                requested.
            expiry_threshold: How long before token expiration should token be
                refreshed when needed. This does not mean that the token will be
                refreshed before it expires, only indicates the earliest moment before
                the expiration when refresh would occur. (default: 5s)
            expires_in_fallback: Fallback value for the expires_in value. Will be used
                when token response does not contains expires_in field.
            minimal_refresh_period: Optionally minimal period between the earliest token
                refresh exchanges.
            http_timeout: The timeout for HTTP requests. Value applies to all of the
                timeouts (connect, read, write).
            http_ssl_context: The SSL context to use for HTTPS requests.
                If not specified default SSL context is used.
        """

        if token_endpoint_url and issuer_url:
            raise ValueError(
                "'token_endpoint_url' and 'issuer_url' arguments are "
                " mutually exclusive. set only one."
            )
        if not token_endpoint_url and not issuer_url:
            raise ValueError(
                "setting 'token_endpoint_url' or 'issuer_url' argument is required."
            )

        self._token_container = token.Container(
            refresh_token=refresh_token,
            expiry_threshold=expiry_threshold,
            expires_in_fallback=expires_in_fallback,
            minimal_expires_in=minimal_refresh_period,
        )

        self._original_refresh_token = refresh_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope

        self._expiry_threshold = expiry_threshold
        self._expires_in_fallback = expires_in_fallback
        self._minimal_refresh_period = minimal_refresh_period

        self._token_endpoint_url = None
        if token_endpoint_url:
            self._token_endpoint_url = token_endpoint_url
        if issuer_url:
            self._issuer_url = issuer_url

        self._http_timeout = http_timeout.total_seconds()
        self._verify = http_ssl_context or ssl.create_default_context()

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
            self._token_endpoint_url, data=self._create_refresh_request_data()
        )

    def _update_token(self, resp: httpx.Response):
        resp_data = resp.json()

        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError:
            if resp.status_code != 400 or not resp_data.get("error"):
                raise
            raise error.TokenEndpointError(
                error=resp_data["error"],
                error_description=resp_data.get("error_description"),
                error_uri=resp_data.get("error_uri"),
            ) from None

        self._token_container.update_token(
            access_token=resp_data["access_token"],
            refresh_token=resp_data.get("refresh_token"),
            expires_in=resp_data.get("expires_in"),
            scope=resp_data.get("scope"),
        )

    def _update_token_endpoint(self, resp: httpx.Response):
        resp.raise_for_status()
        self._token_endpoint_url = resp.json()["token_endpoint"]

    def _clone(self, constructor, scope: Optional[str] = None):
        issuer_url = None
        if not self._token_endpoint_url:
            issuer_url = self._issuer_url

        return constructor(
            refresh_token=self._original_refresh_token,
            client_id=self._client_id,
            issuer_url=issuer_url,
            token_endpoint_url=self._token_endpoint_url,
            client_secret=self._client_secret,
            scope=scope or self._scope,
            expiry_threshold=self._expiry_threshold,
            expires_in_fallback=self._expires_in_fallback,
            minimal_refresh_period=self._minimal_refresh_period,
        )


class TokenProvider(_BaseTokenProvider):
    """Returns access token when called and makes sure that unexpired access token is
    available."""

    def __call__(self) -> str:
        return str(self.token())

    def token(self) -> token.Token:
        self._ensure_token_endpoint_url()
        if self._token_container.refresh_required():
            self._do_refresh()
        return self._token_container.access_token

    def _ensure_token_endpoint_url(self):
        if not self._token_endpoint_url:
            with self._client() as client:
                resp = self._fetch_discovery(client)
            self._update_token_endpoint(resp)

    def _do_refresh(self):
        with self._client() as client:
            resp = self._fetch_token(client)
        self._update_token(resp)

    def _client(self) -> httpx.Client:
        return httpx.Client(timeout=self._http_timeout, verify=self._verify)

    def as_async(self) -> "AsyncTokenProvider":
        """Returns new instance of the asynchronous variant of the token provider
        with the same configuration.
        """
        return self._clone(AsyncTokenProvider)

    def with_scope(self, scope: str) -> "TokenProvider":
        """Returns new instance the token provider for the differently scoped
        access tokens with the same configuration.
        """
        return self._clone(TokenProvider, scope=scope)


class AsyncTokenProvider(_BaseTokenProvider):
    """Returns access token when called and makes sure that unexpired access token is
    available."""

    async def __call__(self) -> str:
        return str(await self.token())

    async def token(self) -> token.Token:
        await self._ensure_token_endpoint_url()
        if self._token_container.refresh_required():
            await self._do_refresh()
        return self._token_container.access_token

    async def _ensure_token_endpoint_url(self):
        if not self._token_endpoint_url:
            async with self._client() as client:
                resp = await self._fetch_discovery(client)
            self._update_token_endpoint(resp)

    async def _do_refresh(self):
        async with self._client() as client:
            resp = await self._fetch_token(client)
        self._update_token(resp)

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=self._http_timeout, verify=self._verify)

    def as_sync(self) -> TokenProvider:
        """Returns new instance of the synchronous variant of the token provider
        with the same configuration.
        """
        return self._clone(TokenProvider)

    def with_scope(self, scope: str) -> "AsyncTokenProvider":
        """Returns new instance the token provider for the differently scoped
        access tokens with the same configuration.
        """
        return self._clone(AsyncTokenProvider, scope=scope)
