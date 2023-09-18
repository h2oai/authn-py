import abc

import h2o_discovery
from h2o_discovery import model
import pytest
import respx
import time_machine

import h2o_authn
import h2o_authn.discovery

TEST_CLIENT_ID = "test-client-id"
TOKEN_ENDPOINT_URL = "http://example.com/token"
ISSUER_URL = "http://example.com/"
ISSUER_DISCOVERY_URL = "http://example.com/.well-known/openid-configuration"

PLATFORM_CLIENT_ID = "test-platfrom-client-id"
PLATFORM_CLIENT_REFRESH_TOKEN = "platform_client_refresh_token"
TEST_CLIENT_REFRESH_TOKEN = "test_client_refresh_token"

TEST_DISCOVERY = h2o_discovery.Discovery(
    environment=model.Environment(
        issuer_url=ISSUER_URL,
        h2o_cloud_environment="https://example.com",
        h2o_cloud_platform_oauth2_scope="input scope",
        h2o_cloud_version="TEST",
    ),
    clients={
        "platform": model.Client(
            name="platform",
            oauth2_client_id=PLATFORM_CLIENT_ID,
            display_name="Platform Test Client",
        ),
        "test_client": model.Client(
            name="test_client",
            oauth2_client_id=TEST_CLIENT_ID,
            display_name="Test Client",
        ),
    },
    services={
        "test-service": model.Service(
            name="test-service",
            oauth2_scope="test service scopes",
            display_name="Test Service",
            uri="https://example.com",
            python_client="test-service",
            version="TEST",
        )
    },
    credentials={
        "platform": model.Credentials(
            client="platform", refresh_token=PLATFORM_CLIENT_REFRESH_TOKEN
        ),
        "test_client": model.Credentials(
            client="test_client", refresh_token=TEST_CLIENT_REFRESH_TOKEN
        ),
    },
)


class AbstractTestCase(abc.ABC):
    @abc.abstractmethod
    def given(self):
        pass

    @abc.abstractmethod
    def then(self):
        pass


class SyncTestCase:
    provider: h2o_authn.TokenProvider

    @staticmethod
    def create_provider(*args, **kwargs):
        return h2o_authn.TokenProvider(*args, **kwargs)

    @staticmethod
    def create_provider_from_discovery(*args, **kwargs):
        return h2o_authn.discovery.create(*args, **kwargs)

    def when(self):
        with time_machine.travel(0, tick=False):
            self.token = self.provider.token()


class AsyncTestCase:
    provider: h2o_authn.AsyncTokenProvider

    @staticmethod
    def create_provider(*args, **kwargs):
        return h2o_authn.AsyncTokenProvider(*args, **kwargs)

    @staticmethod
    def create_provider_from_discovery(*args, **kwargs):
        return h2o_authn.discovery.create_async(*args, **kwargs)

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
        self.issuer_discovery_route = respx.get(ISSUER_DISCOVERY_URL).respond(
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
        assert self.issuer_discovery_route.called
        assert self.token_route.called


class ProviderFromDiscoveryWithDefaultClient(AbstractTestCase):
    def given(self):
        self.issuer_discovery_route = respx.get(ISSUER_DISCOVERY_URL).respond(
            json={"token_endpoint": TOKEN_ENDPOINT_URL}
        )

        self.token_route = respx.post(
            TOKEN_ENDPOINT_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": PLATFORM_CLIENT_ID,
                "refresh_token": PLATFORM_CLIENT_REFRESH_TOKEN,
            },
        ).respond(json={"access_token": "new_access_token"})

        self.provider = self.create_provider_from_discovery(discovery=TEST_DISCOVERY)

    def then(self):
        assert self.issuer_discovery_route.called
        assert self.token_route.called


class ProviderFromDiscoveryWithExplicitClient(AbstractTestCase):
    def given(self):
        self.issuer_discovery_route = respx.get(ISSUER_DISCOVERY_URL).respond(
            json={"token_endpoint": TOKEN_ENDPOINT_URL}
        )

        self.token_route = respx.post(
            TOKEN_ENDPOINT_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": TEST_CLIENT_ID,
                "refresh_token": TEST_CLIENT_REFRESH_TOKEN,
            },
        ).respond(json={"access_token": "new_access_token"})

        self.provider = self.create_provider_from_discovery(
            discovery=TEST_DISCOVERY, client="test_client"
        )

    def then(self):
        assert self.issuer_discovery_route.called
        assert self.token_route.called


class ProviderFromDiscoveryWithScope(AbstractTestCase):
    def given(self):
        self.issuer_discovery_route = respx.get(ISSUER_DISCOVERY_URL).respond(
            json={"token_endpoint": TOKEN_ENDPOINT_URL}
        )

        self.token_route = respx.post(
            TOKEN_ENDPOINT_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": PLATFORM_CLIENT_ID,
                "refresh_token": PLATFORM_CLIENT_REFRESH_TOKEN,
                "scope": "explicit scope",
            },
        ).respond(json={"access_token": "new_access_token"})

        self.provider = self.create_provider_from_discovery(
            discovery=TEST_DISCOVERY, scope="explicit scope"
        )

    def then(self):
        assert self.issuer_discovery_route.called
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
