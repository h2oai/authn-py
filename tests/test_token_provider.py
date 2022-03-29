from copyreg import constructor
import pytest

import h2o_authn


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
