import datetime
import ssl
from typing import Optional

import h2o_discovery

from h2o_authn import provider

DEFAULT_CLIENT = "platform"


def create(
    discovery: h2o_discovery.Discovery,
    client: str = DEFAULT_CLIENT,
    *,
    scope: Optional[str] = None,
    client_secret: Optional[str] = None,
    expiry_threshold: datetime.timedelta = provider.DEFAULT_EXPIRY_THRESHOLD,
    expires_in_fallback: datetime.timedelta = provider.DEFAULT_EXPIRES_IN_FALLBACK,
    http_timeout: datetime.timedelta = provider.DEFAULT_HTTP_TIMEOUT,
    minimal_refresh_period: Optional[datetime.timedelta] = None,
    http_ssl_context: Optional[ssl.SSLContext] = None,
):
    """Returns a new TokenProvider instance configured from the given Discovery object.

    By default the provider will be configured to use the "platform".

    Args:
        discovery: The Discovery object to use for configuration.
        client: The name of the client to use for configuration.
            Defaults to "platform".
        scope: The scope to use for the token requests.
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

    client_id = discovery.clients[client].oauth2_client_id
    issuer_url = discovery.environment.issuer_url
    refresh_token = discovery.credentials[client].refresh_token

    return provider.TokenProvider(
        refresh_token=refresh_token,
        client_id=client_id,
        issuer_url=issuer_url,
        client_secret=client_secret,
        scope=scope,
        expiry_threshold=expiry_threshold,
        expires_in_fallback=expires_in_fallback,
        http_timeout=http_timeout,
        minimal_refresh_period=minimal_refresh_period,
        http_ssl_context=http_ssl_context,
    )


def create_async(
    discovery: h2o_discovery.Discovery,
    client: str = DEFAULT_CLIENT,
    *,
    scope: Optional[str] = None,
    client_secret: Optional[str] = None,
    expiry_threshold: datetime.timedelta = provider.DEFAULT_EXPIRY_THRESHOLD,
    expires_in_fallback: datetime.timedelta = provider.DEFAULT_EXPIRES_IN_FALLBACK,
    http_timeout: datetime.timedelta = provider.DEFAULT_HTTP_TIMEOUT,
    minimal_refresh_period: Optional[datetime.timedelta] = None,
    http_ssl_context: Optional[ssl.SSLContext] = None,
):
    """Returns a new AsyncTokenProvider instance configured from the given Discovery
    object.

    By default the provider will be configured to use the "platform".

    Args:
        discovery: The Discovery object to use for configuration.
        client: The name of the client to use for configuration.
            Defaults to "platform".
        scope: The scope to use for the token requests.
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

    client_id = discovery.clients[client].oauth2_client_id
    issuer_url = discovery.environment.issuer_url
    refresh_token = discovery.credentials[client].refresh_token

    return provider.AsyncTokenProvider(
        refresh_token=refresh_token,
        client_id=client_id,
        issuer_url=issuer_url,
        client_secret=client_secret,
        scope=scope,
        expiry_threshold=expiry_threshold,
        expires_in_fallback=expires_in_fallback,
        minimal_refresh_period=minimal_refresh_period,
        http_timeout=http_timeout,
        http_ssl_context=http_ssl_context,
    )
