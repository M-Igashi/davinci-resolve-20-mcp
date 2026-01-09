"""Core module for DaVinci Resolve MCP Server."""

from .connection import ResolveConnection, get_resolve
from .decorators import (
    handle_resolve_errors,
    require_media_pool,
    require_project,
    require_resolve,
    require_timeline,
    validate_params,
    with_page,
)
from .errors import (
    NoMediaPoolError,
    NoProjectError,
    NotConnectedError,
    NoTimelineError,
    ResolveError,
)

__all__ = [
    "ResolveConnection",
    "get_resolve",
    "handle_resolve_errors",
    "require_resolve",
    "require_project",
    "require_timeline",
    "require_media_pool",
    "validate_params",
    "with_page",
    "ResolveError",
    "NotConnectedError",
    "NoProjectError",
    "NoTimelineError",
    "NoMediaPoolError",
]
