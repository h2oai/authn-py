# `h2o-authn`

[![licence](https://img.shields.io/github/license/h2oai/authn-py?style=flat-square)](https://github.com/h2oai/authn-py/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/h2o-authn?style=flat-square)](https://pypi.org/project/h2o-authn/)

H2O Python Clients Authentication Helpers.

## Installation

```sh
pip install h2o-authn
```

## Usage

Package provides two top level classes `h2o_authn.TokenProvider` and `h2o_authn.AsyncTokenProvider` with identical constructors accepting following arguments:

- `refresh_token`: Refresh token which will used for the access token exchange.
- `client_id`: OAuth 2.0 client id that will be used or the access token
    exchange.
- `issuer_url` or `token_endpoint_url` **needs to be provided**
  - `issuer_url`: Base URL of the issuer. This URL will be used for the discovery
        to obtain token endpoint. Mutually exclusive with the
        token_endpoint_url argument.
  - `token_endpoint_url`: URL of the token endpoint that should be used for the
        access token exchange. Mutually exclusive with the issuer_url argument.
- `client_secret`: Optional OAuth 2.0 client secret for the confidential
    clients. Used only when provided.
- `scope`: Optionally sets the the scope for which the access token should be
    requested.
- `expiry_threshold`: How long before token expiration should token be
    refreshed when needed. This does not mean that the token will be
    refreshed before it expires, only indicates the earliest moment before
    the expiration when refresh would occur. (default: 5s)
- `expires_in_fallback`: Fallback value for the expires_in value. Will be used
    when token response does not contains expires_in field.
- `minimal_refresh_period`: Optionally minimal period between the earliest token
    refresh exchanges.

Both classes has identical interface in sync or async variant.

```python
provider = h2o_authn.TokenProvider(...)
aprovider = h2o_authn.AsyncTokenProvider(...)


# Calling the providers directly makes sure that fresh access token is available
# and returns it.
access_token = provider()
access_token = await aprovider()


# Calling the token() returns h2o_authn.token.Token instance.
token = provider.token()
token = await aprovider.token()

# It can used as str.
assert token == access_token

# And contains additional attributes when available.
token.exp  # Is expiration of the token as datetime.datetime
token.scope  # Is scope of the token if server provided it.


# Sync/Async variants can be converted from one to another.
provider = aprovider.as_sync()
aprovider = provider.as_async()


# When access token with different scope is needed new instance can cloned from
# the current with different scope.
provider = provider.with_scope("new scopes")
aprovider = aprovider.with_scope("new scopes")
```

### Examples

#### Example: Use with H2O.ai MLOps Python CLient

```python
import h2o_authn
import h2o_mlops_client as mlops

provider = h2o_authn.TokenProvider(...)
mlops_client = mlops.Client(
    gateway_url="https://mlops-api.cloud.h2o.ai",
    token_provider=provider,
)
...
```

#### Example: Use with H2O.ai Drive Python Client within the Wave App

```python
import h2o_authn
import h2o_drive
from h2o_wave import Q, app, ui
from h2o_wave import main

@app("/")
async def serve(q: Q):
    provider = h2o_authn.AsyncTokenProvider(
        refresh_token=q.auth.refresh_token,
        issuer_url=os.getenv("H2O_WAVE_OIDC_PROVIDER_URL"),
        client_id=os.getenv("H2O_WAVE_OIDC_CLIENT_ID"),
        client_secret=os.getenv("H2O_WAVE_OIDC_CLIENT_SECRET"),
    )
    my_home = await h2o_drive.MyHome(token=provider)

    ...
```

#### Example: Use with H2O.ai Enterprise Steam Python Client

```python
import h2o_authn
import h2osteam
import h2osteam.clients

provider = h2o_authn.TokenProvider(...)

h2osteam.login(
    url="https://steam.cloud-dev.h2o.ai", access_token=provider()
)
client = h2osteam.clients.DriverlessClient()

...
```

### H2O Cloud Discovery support

I you use the token provider to access H2O.ai services running in your  H2O AI Cloud environment, you
can simply the configuration by using `h2o-authn[discovery]` extension.

For more info regarding H2O Cloud Discovery, please see
[H2O Cloud Discovery Client](https://github.com/h2oai/cloud-discovery-py)

```sh
pip install h2o-authn[discovery]
```

Module `h2o_authn.discovery` provides `new` and `new_async` functions which
accepts following arguments:

- `discovery`: The Discovery object to use for configuration.
- `client`: The name of the client to use for configuration.
    Defaults to "platform".
- `scope`: The scope to use for the token requests.
- `expiry_threshold`: How long before token expiration should token be
    refreshed when needed. This does not mean that the token will be
    refreshed before it expires, only indicates the earliest moment before
    the expiration when refresh would occur. (default: 5s)
- `expires_in_fallback`: Fallback value for the expires_in value. Will be used
    when token response does not contains expires_in field.
- `minimal_refresh_period`: Optionally minimal period between the earliest token
    refresh exchanges.

#### Example: Use of the H2O Cloud Discovery with H2O.ai MLOps Python CLient

```python

import h2o_authn.discovery
import h2o_discovery
import h2o_mlops_client as mlops


discovery = h2o_discovery.discover()

provider = h2o_authn.discovery.create(discovery)

mlops_client = mlops.Client(
    gateway_url=discovery.services["mlops-api"].uri,
    token_provider=provider,
)
...
```
