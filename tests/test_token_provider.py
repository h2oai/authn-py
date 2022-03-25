import h2o_authn


def test_provider():
    # Given
    provider = h2o_authn.TokenProvider(
        refresh_token="test-refresh-token", client_id="test-client-d"
    )

    # When
