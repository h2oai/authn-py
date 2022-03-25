import datetime
from typing import Optional

DEFAULT_EXPIRY_THRESHOLD = datetime.timedelta(seconds=5)
DEFAULT_EXPIRES_IN_FALLBACK = datetime.timedelta(seconds=30)


class Token(str):
    exp: datetime.datetime
    scope: Optional[str]

    def __new__(cls, value: str, exp: datetime.datetime, scope: Optional[str]):
        token = str(value)
        setattr(token, "exp", exp)
        setattr(token, "scope", scope)
        return token


class Container:
    def __init__(
        self,
        *,
        refresh_token: str,
        scope: Optional[str] = None,
        expiry_threshold: datetime.timedelta = DEFAULT_EXPIRY_THRESHOLD,
        expires_in_fallback: datetime.timedelta = DEFAULT_EXPIRES_IN_FALLBACK,
        minimal_expires_in: Optional[datetime.timedelta] = None,
    ) -> None:

        self._original_access_token = refresh_token
        self._refresh_token = refresh_token
        self._original_access_token = refresh_token
        self._expiry_threshold = expiry_threshold
        self._expires_in_fallback = expires_in_fallback
        self._minimal_expires_in = minimal_expires_in
        self._scope = scope

        self._access_token: Optional[Token] = None
        self._access_token_exp: Optional[datetime.datetime] = None

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @property
    def access_token(self) -> Token:
        if not self._access_token:
            raise AttributeError("access_token not initiliazed yet")
        return self._access_token

    def refresh_required(self) -> bool:
        if self._access_token is None or self._access_token_exp is None:
            return True

        now = datetime.datetime.now(datetime.timezone.utc)
        return self._access_token_exp <= (now + self._expiry_threshold)

    def update_token(
        self,
        access_token: str,
        expires_in: Optional[int],
        refresh_token: Optional[str],
        scope: Optional[str],
    ):
        exp_delta = self._expires_in_fallback
        if expires_in:
            exp_delta = datetime.timedelta(seconds=expires_in)

        now = datetime.datetime.now(datetime.timezone.utc)
        exp = now + exp_delta
        token_scope = scope or self._scope

        if refresh_token:
            self._refresh_token = refresh_token

        self._access_token = Token(access_token, exp=exp, scope=token_scope)
        self._access_token_exp = exp
        if self._minimal_expires_in:
            self._access_token_exp = min(exp, now + self._minimal_expires_in)
