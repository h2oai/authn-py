import datetime

import pytest
import time_machine

from h2o_authn import token


def test_refresh_token_provided():
    # Given
    refresh_token = "test-refresh-token"

    # When
    container = token.Container(refresh_token=refresh_token)

    # Then
    assert container.refresh_token == refresh_token


def test_access_token_property_fails_before_update():
    # Given
    container = token.Container(refresh_token="test-refresh-token")

    # When
    with pytest.raises(AttributeError) as exc_info:
        _ = container.access_token

    # Then
    assert str(exc_info.value) == "access_token not initiliazed yet"


def test_refresh_required_after_init():
    # Given
    container = token.Container(refresh_token="test-refresh-token")

    # When
    result = container.refresh_required()

    # Then
    assert result is True


def test_refresh_not_required_before_expiry():
    # Given
    container = token.Container(refresh_token="test-refresh-token")

    # When
    with time_machine.travel(0) as traveler:
        container.update_token("test-access_token", expires_in=3600)
        traveler.shift(datetime.timedelta(seconds=1800))
        result = container.refresh_required()

    # Then
    assert result is False


def test_refresh_required_within_expiry_treshold():
    # Given
    container = token.Container(
        refresh_token="test-refresh-token",
        expiry_threshold=datetime.timedelta(seconds=2000),
    )

    # When
    with time_machine.travel(0) as traveler:
        container.update_token("test-access_token", expires_in=3600)
        traveler.shift(datetime.timedelta(seconds=1800))
        result = container.refresh_required()

    # Then
    assert result is True


def test_refresh_not_required_before_minimal_expires_in():
    # Given
    container = token.Container(
        refresh_token="test-refresh-token",
        expiry_threshold=datetime.timedelta(seconds=0),
        minimal_expires_in=datetime.timedelta(seconds=1800),
    )

    # When
    with time_machine.travel(0) as traveler:
        container.update_token("test-access_token", expires_in=3600)
        traveler.shift(datetime.timedelta(seconds=900))
        result = container.refresh_required()

    # Then
    assert result is False


def test_refresh_required_after_minimal_expires_in():
    # Given
    container = token.Container(
        refresh_token="test-refresh-token",
        expiry_threshold=datetime.timedelta(seconds=0),
        minimal_expires_in=datetime.timedelta(seconds=1800),
    )

    # When
    with time_machine.travel(0) as traveler:
        container.update_token("test-access_token", expires_in=3600)
        traveler.shift(datetime.timedelta(seconds=1800))
        result = container.refresh_required()

    # Then
    assert result is True


def test_refresh_not_required_before_expires_in_fallback():
    # Given
    container = token.Container(
        refresh_token="test-refresh-token",
        expiry_threshold=datetime.timedelta(seconds=0),
        expires_in_fallback=datetime.timedelta(seconds=3600),
    )

    # When
    with time_machine.travel(0) as traveler:
        container.update_token("test-access_token")
        traveler.shift(datetime.timedelta(seconds=1800))
        result = container.refresh_required()

    # Then
    assert result is False


def test_refresh_required_after_expires_in_fallback():
    # Given
    container = token.Container(
        refresh_token="test-refresh-token",
        expiry_threshold=datetime.timedelta(seconds=0),
        expires_in_fallback=datetime.timedelta(seconds=3600),
    )

    # When
    with time_machine.travel(0) as traveler:
        container.update_token("test-access_token")
        traveler.shift(datetime.timedelta(seconds=3600))
        result = container.refresh_required()

    # Then
    assert result is True


def test_update_token_values_utilized():
    # Given
    container = token.Container(refresh_token="test-refresh-token")

    # When
    with time_machine.travel(0):
        container.update_token("test-access-token", expires_in=3600, scope="new-scope")
        access_token = container.access_token

    # Then
    assert access_token == "test-access-token"
    assert access_token.exp.timestamp() == 3600
    assert access_token.scope == "new-scope"


def test_update_token_refresh_token_used():
    # Given
    container = token.Container(refresh_token="old-refresh-token")
    container.update_token("test-access-token", refresh_token="new-refresh-token")

    # When
    refresh_token = container.refresh_token

    # Then
    assert refresh_token == "new-refresh-token"
