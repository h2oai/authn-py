from typing import Optional


class BaseException(Exception):
    pass


class TokenEndpointError(BaseException):
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
            parts.append(f", error_description={self.error_uri!r}")
        parts.append(")")
        return "".join(parts)
