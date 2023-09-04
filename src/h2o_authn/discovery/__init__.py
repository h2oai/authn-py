import datetime
from typing import Optional

import h2o_discovery

from h2o_authn import provider

DEFAULT_CLIENT = "platform"


def new(
    discovery: h2o_discovery.Discovery,
    client: str = DEFAULT_CLIENT,
    *,
    service: Optional[str] = None,
    scope: Optional[str] = None,
    client_secret: Optional[str] = None,
    expiry_threshold: datetime.timedelta = provider.DEFAULT_EXPIRY_THRESHOLD,
    expires_in_fallback: datetime.timedelta = provider.DEFAULT_EXPIRES_IN_FALLBACK,
    minimal_refresh_period: Optional[datetime.timedelta] = None,
):
    client_id = discovery.clients[client].oauth2_client_id
    issuer_url = discovery.environment.issuer_url
    refresh_token = discovery.credentials[client].refresh_token

    set_scope = scope
    if not set_scope and service:
        set_scope = discovery.services[service].oauth2_scope

    return provider.TokenProvider(
        refresh_token=refresh_token,
        client_id=client_id,
        issuer_url=issuer_url,
        client_secret=client_secret,
        scope=set_scope,
        expiry_threshold=expiry_threshold,
        expires_in_fallback=expires_in_fallback,
        minimal_refresh_period=minimal_refresh_period,
    )


def new_async(
    discovery: h2o_discovery.Discovery,
    client: str = DEFAULT_CLIENT,
    *,
    service: Optional[str] = None,
    scope: Optional[str] = None,
    client_secret: Optional[str] = None,
    expiry_threshold: datetime.timedelta = provider.DEFAULT_EXPIRY_THRESHOLD,
    expires_in_fallback: datetime.timedelta = provider.DEFAULT_EXPIRES_IN_FALLBACK,
    minimal_refresh_period: Optional[datetime.timedelta] = None,
):
    client_id = discovery.clients[client].oauth2_client_id
    issuer_url = discovery.environment.issuer_url
    refresh_token = discovery.credentials[client].refresh_token

    set_scope = scope
    if not set_scope and service:
        set_scope = discovery.services[service].oauth2_scope

    return provider.AsyncTokenProvider(
        refresh_token=refresh_token,
        client_id=client_id,
        issuer_url=issuer_url,
        client_secret=client_secret,
        scope=set_scope,
        expiry_threshold=expiry_threshold,
        expires_in_fallback=expires_in_fallback,
        minimal_refresh_period=minimal_refresh_period,
    )
