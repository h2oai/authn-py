from typing import Optional


class BaseError(Exception):
    """Base class for the exceptions raised by the package."""


class TokenEndpointError(BaseError):
    """Thrown when token providers catch well defined error sent back by server."""

    error: str
    error_description: Optional[str]
    error_uri: Optional[str]

    def __init__(
        self,
        *,
        error: str,
        error_description: Optional[str] = None,
        error_uri: Optional[str] = None,
    ) -> None:
        self.error = error
        self.error_description = error_description
        self.error_uri = error_uri

    def __repr__(self) -> str:
        parts = [f"TokenEndpointError(error={self.error!r}"]
        if self.error_description:
            parts.append(f", error_description={self.error_description!r}")
        if self.error_uri:
            parts.append(f", error_uri={self.error_uri!r}")
        parts.append(")")
        return "".join(parts)

    def __str__(self) -> str:
        parts = [self.error]
        if self.error_description:
            parts.append(f": {self.error_description}")
        if self.error_uri:
            parts.append(f" ({self.error_uri})")
        return "".join(parts)
