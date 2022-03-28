import collections
import datetime
from typing import Optional

DEFAULT_EXPIRY_THRESHOLD = datetime.timedelta(seconds=5)
DEFAULT_EXPIRES_IN_FALLBACK = datetime.timedelta(seconds=30)


class Token(collections.UserString):
    """Represents token returned by the providers.

    Extends strings type and allows to check exp and scope of the token.
    """

    def __init__(
        self, value: str, exp: datetime.datetime, scope: Optional[str]
    ) -> None:
        super().__init__(value)
        self._exp = exp
        self._scope = scope

    @property
    def exp(self):
        return self._exp

    @property
    def scope(self):
        return self._scope


class Container:
    """Manages data required for token updating.

    Used by the providers to check how the token should be refreshed.
    """

    def __init__(
        self,
        refresh_token: str,
        *,
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

        self._access_token: Optional[Token] = None
        self._access_token_exp: Optional[datetime.datetime] = None

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @property
    def original_refresh_token(self) -> str:
        return self._original_access_token

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
        expires_in: Optional[int] = None,
        refresh_token: Optional[str] = None,
        scope: Optional[str] = None,
    ):
        exp_delta = self._expires_in_fallback
        if expires_in:
            exp_delta = datetime.timedelta(seconds=expires_in)

        now = datetime.datetime.now(datetime.timezone.utc)
        exp = now + exp_delta

        if refresh_token:
            self._refresh_token = refresh_token

        self._access_token = Token(access_token, exp=exp, scope=scope)
        self._access_token_exp = exp
        if self._minimal_expires_in:
            self._access_token_exp = min(exp, now + self._minimal_expires_in)
