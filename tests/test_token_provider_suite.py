import abc

import pytest
import respx
import time_machine

import h2o_authn

TEST_CLIENT_ID = "test-client-id"
TOKEN_ENDPOINT_URL = "http://example.com/token"
ISSUER_URL = "http://example.com/"
ISSUER_DISCOVERY_URL = "http://example.com/.well-known/openid-configuration"


class AbstractTestCase(abc.ABC):
    @abc.abstractmethod
    def given(self):
        pass

    @abc.abstractmethod
    def then(self):
        pass


class SyncTestCase:
    provider: h2o_authn.TokenProvider
    create_provider = h2o_authn.TokenProvider

    def when(self):
        with time_machine.travel(0, tick=False):
            self.token = self.provider.token()


class AsyncTestCase:
    provider: h2o_authn.AsyncTokenProvider
    create_provider = h2o_authn.AsyncTokenProvider

    async def when(self):
        with time_machine.travel(0, tick=False):
            self.token = await self.provider.token()


class ProviderTest(AbstractTestCase):
    def given(self):
        self.route = respx.post(
            TOKEN_ENDPOINT_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": TEST_CLIENT_ID,
                "refresh_token": "input_refresh_token",
            },
        ).respond(
            json={
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "scope": "new scope",
                "expires_in": 3600,
            }
        )

        self.provider = self.create_provider(
            refresh_token="input_refresh_token",
            client_id=TEST_CLIENT_ID,
            token_endpoint_url=TOKEN_ENDPOINT_URL,
        )

    def then(self):
        assert self.route.called

        assert self.token == "new_access_token"
        assert self.token.scope == "new scope"
        assert self.token.exp.timestamp() == 3600


class ProviderTestOptionalParamsUsed(AbstractTestCase):
    def given(self):
        self.route = respx.post(
            TOKEN_ENDPOINT_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": TEST_CLIENT_ID,
                "refresh_token": "input_refresh_token",
                "client_secret": "input_client_secret",
                "scope": "input scope",
            },
        ).respond(json={"access_token": "new_access_token"})

        self.provider = self.create_provider(
            refresh_token="input_refresh_token",
            client_secret="input_client_secret",
            scope="input scope",
            client_id=TEST_CLIENT_ID,
            token_endpoint_url=TOKEN_ENDPOINT_URL,
        )

    def then(self):
        assert self.route.called


class ProviderTestIssuerDiscoveryUsed(AbstractTestCase):
    def given(self):
        self.discovery_route = respx.get(ISSUER_DISCOVERY_URL).respond(
            json={"token_endpoint": TOKEN_ENDPOINT_URL}
        )

        self.token_route = respx.post(
            TOKEN_ENDPOINT_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": TEST_CLIENT_ID,
                "refresh_token": "input_refresh_token",
            },
        ).respond(json={"access_token": "new_access_token"})

        self.provider = self.create_provider(
            refresh_token="input_refresh_token",
            client_id=TEST_CLIENT_ID,
            issuer_url=ISSUER_URL,
        )

    def then(self):
        assert self.discovery_route.called
        assert self.token_route.called


def _all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in _all_subclasses(c)]
    )


@pytest.fixture(scope="module", params=_all_subclasses(AbstractTestCase))
def sync_case(request):
    class TC(request.param, SyncTestCase):
        pass

    yield TC()


@pytest.fixture(scope="module", params=_all_subclasses(AbstractTestCase))
def async_case(request):
    class TC(request.param, AsyncTestCase):
        pass

    yield TC()


@respx.mock
def test_sync_token_provider(sync_case):
    sync_case.given()
    sync_case.when()
    sync_case.then()


@respx.mock
@pytest.mark.asyncio
async def test_async_token_provider(async_case):
    async_case.given()
    await async_case.when()
    async_case.then()
