import pytest

import h2o_authn.error


def repr_test_cases():
    yield pytest.param(
        "TEST_ERROR",
        "Test Description.",
        "https://example.com/error",
        (
            "TokenEndpointError(error='TEST_ERROR', "
            "error_description='Test Description.', "
            "error_uri='https://example.com/error')"
        ),
        id="all",
    )
    yield pytest.param(
        "TEST_ERROR",
        "Test Description.",
        None,
        (
            "TokenEndpointError(error='TEST_ERROR', "
            "error_description='Test Description.')"
        ),
        id="no error uri",
    )
    yield pytest.param(
        "TEST_ERROR",
        None,
        "https://example.com/error",
        (
            "TokenEndpointError(error='TEST_ERROR', "
            "error_uri='https://example.com/error')"
        ),
        id="no error description",
    )
    yield pytest.param(
        "TEST_ERROR",
        None,
        None,
        "TokenEndpointError(error='TEST_ERROR')",
        id="error only",
    )


@pytest.mark.parametrize("error, error_description, error_uri, want", repr_test_cases())
def test_repr(error, error_description, error_uri, want):
    # Given
    error = h2o_authn.error.TokenEndpointError(
        error=error, error_description=error_description, error_uri=error_uri
    )

    # When
    result = repr(error)

    # Then
    assert result == want


def str_test_cases():
    yield pytest.param(
        "TEST_ERROR",
        "Test Description.",
        "https://example.com/error",
        "TEST_ERROR: Test Description. (https://example.com/error)",
        id="all",
    )
    yield pytest.param(
        "TEST_ERROR",
        "Test Description.",
        None,
        "TEST_ERROR: Test Description.",
        id="no error uri",
    )
    yield pytest.param(
        "TEST_ERROR",
        None,
        "https://example.com/error",
        "TEST_ERROR (https://example.com/error)",
        id="no error description",
    )
    yield pytest.param("TEST_ERROR", None, None, "TEST_ERROR", id="error only")


@pytest.mark.parametrize("error, error_description, error_uri, want", str_test_cases())
def test_str(error, error_description, error_uri, want):
    # Given
    error = h2o_authn.error.TokenEndpointError(
        error=error, error_description=error_description, error_uri=error_uri
    )

    # When
    result = str(error)

    # Then
    assert result == want
