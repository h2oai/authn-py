import respx
import time_machine
import httpx
import pytest

import h2o_authn


TEST_CLIENT_ID = "test-client-id"
TOKEN_ENDPOINT_URL = "http://example.com/token"


@respx.mock
def test_provider():
    # Given
    route = respx.post(TOKEN_ENDPOINT_URL).mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "scope": "new scope",
                "expires_in": 3600,
            },
        )
    )
    provider = h2o_authn.TokenProvider(
        refresh_token="old_refresh_token",
        client_id=TEST_CLIENT_ID,
        token_endpoint_url=TOKEN_ENDPOINT_URL,
    )

    # When
    with time_machine.travel(0, tick=False):
        token = provider()

    # Then
    assert route.called
    assert token == "new_access_token"
    assert token.scope == "new scope"
    assert token.exp.timestamp() == 3600


@pytest.mark.asyncio
@respx.mock
async def test_async_provider():
    # Given
    route = respx.post(TOKEN_ENDPOINT_URL).mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "scope": "new scope",
                "expires_in": 3600,
            },
        )
    )

    provider = h2o_authn.AsyncTokenProvider(
        refresh_token="old_refresh_token",
        client_id=TEST_CLIENT_ID,
        token_endpoint_url=TOKEN_ENDPOINT_URL,
    )

    # When
    with time_machine.travel(0, tick=False):
        token = await provider()

    # Then
    assert route.called
    assert token == "new_access_token"
    assert token.scope == "new scope"
    assert token.exp.timestamp() == 3600

    assert token == "new_access_token"
