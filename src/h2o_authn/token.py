import collections
import datetime
from typing import Optional

DEFAULT_EXPIRY_THRESHOLD = datetime.timedelta(seconds=5)
DEFAULT_EXPIRES_IN_FALLBACK = datetime.timedelta(seconds=30)


class Token(collections.UserString):
    def __init__(
        self, value: str, exp: Optional[datetime.datetime], scope: Optional[str]
    ) -> None:
        super().__init__(value)
        self._exp = exp
        self._scope = scope

    @property
    def exp(self) -> Optional[datetime.datetime]:
        """Indicates the moment when the token expires."""
        return self._exp

    @property
    def scope(self) -> Optional[str]:
        """Scope of the token if known."""
        return self._scope


class Container:
    def __init__(
        self,
        refresh_token: str,
        *,
        expiry_threshold: datetime.timedelta = DEFAULT_EXPIRY_THRESHOLD,
        expires_in_fallback: datetime.timedelta = DEFAULT_EXPIRES_IN_FALLBACK,
        minimal_expires_in: Optional[datetime.timedelta] = None,
    ) -> None:
        self._original_refresh_token = refresh_token
        self._refresh_token = refresh_token
        self._expiry_threshold = expiry_threshold
        self._expires_in_fallback = expires_in_fallback
        self._minimal_expires_in = minimal_expires_in

        self._access_token: Optional[Token] = None
        self._access_token_exp: Optional[datetime.datetime] = None

    @property
    def refresh_token(self) -> str:
        """Current refresh token."""
        return self._refresh_token

    @property
    def original_refresh_token(self) -> str:
        """Original refresh token passed during the initialization."""
        return self._original_refresh_token

    @property
    def access_token(self) -> Token:
        """Current access token."""
        if not self._access_token:
            raise AttributeError("access_token not initiliazed yet")
        return self._access_token

    def refresh_required(self) -> bool:
        """Returns True when there's no access token set or the current one requires
        refresh.
        """
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
        """Updates the token managed by the container from the fields expected in the
        token endpoint response.
        """
        exp_delta = self._expires_in_fallback
        now = datetime.datetime.now(datetime.timezone.utc)

        token_exp: Optional[datetime.datetime] = None
        if expires_in:
            exp_delta = datetime.timedelta(seconds=expires_in)
            token_exp = now + exp_delta

        exp = now + exp_delta

        if refresh_token:
            self._refresh_token = refresh_token

        self._access_token = Token(access_token, exp=token_exp, scope=scope)
        self._access_token_exp = exp
        if self._minimal_expires_in:
            self._access_token_exp = min(exp, now + self._minimal_expires_in)
