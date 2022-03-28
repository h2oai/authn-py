import datetime

from h2o_authn import token


def test_token():
    # Given
    value = "test-token"
    exp = datetime.datetime.now()
    scope = "test-scope-1 test-scope-2"

    # When
    t = token.Token("test-token", exp=exp, scope=scope)

    # Then
    assert t == value
    assert t.exp == exp
    assert t.scope == scope
