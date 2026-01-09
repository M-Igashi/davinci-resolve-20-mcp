"""Custom exceptions for DaVinci Resolve MCP Server."""


class ResolveError(Exception):
    """Base exception for Resolve-related errors."""

    pass


class NotConnectedError(ResolveError):
    """Raised when not connected to DaVinci Resolve."""

    def __init__(self, message: str = "Not connected to DaVinci Resolve"):
        super().__init__(message)


class NoProjectError(ResolveError):
    """Raised when no project is currently open."""

    def __init__(self, message: str = "No project currently open"):
        super().__init__(message)


class NoTimelineError(ResolveError):
    """Raised when no timeline is currently active."""

    def __init__(self, message: str = "No timeline currently active"):
        super().__init__(message)


class NoMediaPoolError(ResolveError):
    """Raised when media pool is not available."""

    def __init__(self, message: str = "Failed to get Media Pool"):
        super().__init__(message)


class ClipNotFoundError(ResolveError):
    """Raised when a clip is not found."""

    def __init__(self, clip_name: str):
        super().__init__(f"Clip '{clip_name}' not found")
        self.clip_name = clip_name


class TimelineItemNotFoundError(ResolveError):
    """Raised when a timeline item is not found."""

    def __init__(self, item_id: str):
        super().__init__(f"Timeline item with ID '{item_id}' not found")
        self.item_id = item_id


class InvalidParameterError(ResolveError):
    """Raised when an invalid parameter is provided."""

    def __init__(self, param_name: str, valid_values: list = None):
        msg = f"Invalid value for '{param_name}'"
        if valid_values:
            msg += f". Must be one of: {', '.join(str(v) for v in valid_values)}"
        super().__init__(msg)
        self.param_name = param_name
        self.valid_values = valid_values
