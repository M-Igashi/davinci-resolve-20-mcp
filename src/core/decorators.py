"""
Decorators for DaVinci Resolve MCP tools.

These decorators eliminate boilerplate code by handling common patterns
like connection checking, project validation, and error handling.
"""

import functools
import logging
from typing import Any, Callable, ParamSpec, TypeVar

from .connection import get_resolve
from .errors import NotConnectedError, ResolveError

logger = logging.getLogger("davinci-resolve-mcp")

P = ParamSpec("P")
T = TypeVar("T")


def handle_resolve_errors(func: Callable[P, T]) -> Callable[P, str | T]:
    """
    Decorator that catches ResolveError exceptions and returns error messages.

    Use this for MCP tools that should return error strings instead of raising.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str | T:
        try:
            return func(*args, **kwargs)
        except ResolveError as e:
            logger.error(f"Resolve error in {func.__name__}: {e}")
            return f"Error: {e}"
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            return f"Error: {e}"

    return wrapper


def require_resolve(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator that ensures Resolve connection is available.

    Injects 'conn' keyword argument with the ResolveConnection instance.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        conn = get_resolve()
        if not conn.is_connected:
            raise NotConnectedError()
        kwargs["conn"] = conn
        return func(*args, **kwargs)

    return wrapper


def require_project(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator that ensures a project is open.

    Injects 'conn' and 'project' keyword arguments.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        conn = get_resolve()
        if not conn.is_connected:
            raise NotConnectedError()
        project = conn.current_project  # Raises NoProjectError if none
        kwargs["conn"] = conn
        kwargs["project"] = project
        return func(*args, **kwargs)

    return wrapper


def require_timeline(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator that ensures a timeline is active.

    Injects 'conn', 'project', and 'timeline' keyword arguments.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        conn = get_resolve()
        if not conn.is_connected:
            raise NotConnectedError()
        project = conn.current_project  # Raises NoProjectError if none
        timeline = conn.current_timeline  # Raises NoTimelineError if none
        kwargs["conn"] = conn
        kwargs["project"] = project
        kwargs["timeline"] = timeline
        return func(*args, **kwargs)

    return wrapper


def require_media_pool(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator that ensures media pool is available.

    Injects 'conn', 'project', and 'media_pool' keyword arguments.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        conn = get_resolve()
        if not conn.is_connected:
            raise NotConnectedError()
        project = conn.current_project
        media_pool = conn.media_pool
        kwargs["conn"] = conn
        kwargs["project"] = project
        kwargs["media_pool"] = media_pool
        return func(*args, **kwargs)

    return wrapper


def with_page(page: str):
    """
    Decorator that switches to a specific page before executing.

    Returns to the original page after execution.

    Args:
        page: Page to switch to ('media', 'cut', 'edit', 'fusion', 'color', 'fairlight', 'deliver')
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            conn = get_resolve()
            original_page = conn.get_current_page()

            try:
                if original_page != page:
                    conn.switch_page(page)
                return func(*args, **kwargs)
            finally:
                if original_page and original_page != page:
                    conn.switch_page(original_page)

        return wrapper

    return decorator


def validate_params(**validators: Callable[[Any], bool]):
    """
    Decorator that validates function parameters.

    Args:
        **validators: Dict of param_name -> validator_function

    Example:
        @validate_params(
            color=lambda c: c in VALID_COLORS,
            frame=lambda f: f >= 0
        )
        def add_marker(frame: int, color: str): ...
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # Get function signature to map args to param names
            import inspect

            sig = inspect.signature(func)
            params = list(sig.parameters.keys())

            # Build full kwargs from args + kwargs
            full_kwargs = dict(zip(params, args))
            full_kwargs.update(kwargs)

            # Validate each parameter
            for param_name, validator in validators.items():
                if param_name in full_kwargs:
                    value = full_kwargs[param_name]
                    if value is not None and not validator(value):
                        raise ValueError(
                            f"Invalid value for parameter '{param_name}': {value}"
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator
