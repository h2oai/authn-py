import pytest
import respx

import h2o_authn
import h2o_authn.error

TEST_CLIENT_ID = "test-client-id"
TEST_CLIENT_SECRET = "test-client-secret"
TOKEN_ENDPOINT_URL = "http://example.com/token"


@pytest.mark.parametrize(
    "constructor", [h2o_authn.TokenProvider, h2o_authn.AsyncTokenProvider]
)
def test_token_provider_constructor_only_one_url_allowed(constructor):
    # When
    with pytest.raises(ValueError) as exc_info:
        _ = constructor(
            refresh_token="",
            client_id="",
            issuer_url="//issuer/url",
            token_endpoint_url="//token/endpoint/url",
        )

    # Then
    assert "mutually exclusive" in str(exc_info.value)


@pytest.mark.parametrize(
    "constructor", [h2o_authn.TokenProvider, h2o_authn.AsyncTokenProvider]
)
def test_token_provider_constructor_atleast_one_url_required(constructor):
    # When
    with pytest.raises(ValueError) as exc_info:
        _ = constructor(refresh_token="", client_id="")

    # Then
    assert "argument is required" in str(exc_info.value)


@respx.mock
@pytest.mark.asyncio
async def test_sync_token_provider_as_async():
    # Given
    route = respx.post(
        TOKEN_ENDPOINT_URL,
        data={
            "grant_type": "refresh_token",
            "client_id": TEST_CLIENT_ID,
            "refresh_token": "input_refresh_token",
            "client_secret": TEST_CLIENT_SECRET,
            "scope": "input scope",
        },
    ).respond(json={"access_token": "new_access_token"})

    provider = h2o_authn.TokenProvider(
        refresh_token="input_refresh_token",
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        token_endpoint_url=TOKEN_ENDPOINT_URL,
        scope="input scope",
    )

    # When
    async_provider = provider.as_async()
    _ = await async_provider()

    # Then
    assert route.called


@respx.mock
def test_async_token_provider_as_sync():
    # Given
    route = respx.post(
        TOKEN_ENDPOINT_URL,
        data={
            "grant_type": "refresh_token",
            "client_id": TEST_CLIENT_ID,
            "refresh_token": "input_refresh_token",
            "client_secret": TEST_CLIENT_SECRET,
            "scope": "input scope",
        },
    ).respond(json={"access_token": "new_access_token"})

    provider = h2o_authn.AsyncTokenProvider(
        refresh_token="input_refresh_token",
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        token_endpoint_url=TOKEN_ENDPOINT_URL,
        scope="input scope",
    )

    # When
    async_provider = provider.as_sync()
    _ = async_provider()

    # Then
    assert route.called


@respx.mock
def test_sync_token_provider_with_scope():
    # Given
    route = respx.post(
        TOKEN_ENDPOINT_URL,
        data={
            "grant_type": "refresh_token",
            "client_id": TEST_CLIENT_ID,
            "refresh_token": "input_refresh_token",
            "client_secret": TEST_CLIENT_SECRET,
            "scope": "new scope",
        },
    ).respond(json={"access_token": "new_access_token"})

    provider = h2o_authn.TokenProvider(
        refresh_token="input_refresh_token",
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        token_endpoint_url=TOKEN_ENDPOINT_URL,
        scope="input scope",
    )

    # When
    new_provider = provider.with_scope("new scope")
    _ = new_provider()

    # Then
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_async_token_provider_with_scope():
    # Given
    route = respx.post(
        TOKEN_ENDPOINT_URL,
        data={
            "grant_type": "refresh_token",
            "client_id": TEST_CLIENT_ID,
            "refresh_token": "input_refresh_token",
            "client_secret": TEST_CLIENT_SECRET,
            "scope": "new scope",
        },
    ).respond(json={"access_token": "new_access_token"})

    provider = h2o_authn.AsyncTokenProvider(
        refresh_token="input_refresh_token",
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        token_endpoint_url=TOKEN_ENDPOINT_URL,
        scope="input scope",
    )

    # When
    new_provider = provider.with_scope("new scope")
    _ = await new_provider()

    # Then
    assert route.called


@respx.mock
def test_sync_token_provider_error_wrapped():
    # Given
    route = respx.post(TOKEN_ENDPOINT_URL).respond(
        400,
        json={
            "error": "test-error",
            "error_description": "test error description",
            "error_uri": "test error URI",
        },
    )

    provider = h2o_authn.TokenProvider(
        refresh_token="input_refresh_token",
        client_id=TEST_CLIENT_ID,
        token_endpoint_url=TOKEN_ENDPOINT_URL,
    )

    # When
    with pytest.raises(h2o_authn.error.TokenEndpointError) as exc_info:
        _ = provider()

    # Then
    assert route.called
    assert exc_info.value.error == "test-error"
    assert exc_info.value.error_description == "test error description"
    assert exc_info.value.error_uri == "test error URI"


@respx.mock
@pytest.mark.asyncio
async def test_async_token_provider_error_wrapped():
    # Given
    route = respx.post(TOKEN_ENDPOINT_URL).respond(
        400,
        json={
            "error": "test-error",
            "error_description": "test error description",
            "error_uri": "test error URI",
        },
    )

    provider = h2o_authn.AsyncTokenProvider(
        refresh_token="input_refresh_token",
        client_id=TEST_CLIENT_ID,
        token_endpoint_url=TOKEN_ENDPOINT_URL,
    )

    # When
    with pytest.raises(h2o_authn.error.TokenEndpointError) as exc_info:
        _ = await provider()

    # Then
    assert route.called
    assert exc_info.value.error == "test-error"
    assert exc_info.value.error_description == "test error description"
    assert exc_info.value.error_uri == "test error URI"
