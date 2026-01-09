"""
DaVinci Resolve connection management.

Provides a singleton connection to DaVinci Resolve with lazy initialization
and automatic reconnection support.
"""

import logging
import os
import sys
from typing import Any, Optional

from .errors import NoMediaPoolError, NoProjectError, NotConnectedError, NoTimelineError

logger = logging.getLogger("davinci-resolve-mcp")


class ResolveConnection:
    """
    Singleton class managing connection to DaVinci Resolve.

    Provides cached access to commonly used objects like project manager,
    current project, media pool, and timeline.
    """

    _instance: Optional["ResolveConnection"] = None
    _resolve: Optional[Any] = None

    def __new__(cls) -> "ResolveConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._setup_paths()
        self._connect()

    def _setup_paths(self) -> None:
        """Setup platform-specific paths for DaVinci Resolve API."""
        from src.utils.platform import get_resolve_paths

        paths = get_resolve_paths()
        self._api_path = paths["api_path"]
        self._lib_path = paths["lib_path"]
        self._modules_path = paths["modules_path"]

        os.environ["RESOLVE_SCRIPT_API"] = self._api_path
        os.environ["RESOLVE_SCRIPT_LIB"] = self._lib_path

        if self._modules_path not in sys.path:
            sys.path.insert(0, self._modules_path)

    def _connect(self) -> None:
        """Establish connection to DaVinci Resolve."""
        try:
            import DaVinciResolveScript as dvr_script

            self._resolve = dvr_script.scriptapp("Resolve")

            if self._resolve:
                logger.info(
                    f"Connected to DaVinci Resolve: "
                    f"{self._resolve.GetProductName()} {self._resolve.GetVersionString()}"
                )
            else:
                logger.error(
                    "Failed to get Resolve object. Is DaVinci Resolve running?"
                )
        except ImportError as e:
            logger.error(f"Failed to import DaVinciResolveScript: {e}")
            self._resolve = None
        except Exception as e:
            logger.error(f"Unexpected error connecting to Resolve: {e}")
            self._resolve = None

    def reconnect(self) -> bool:
        """Attempt to reconnect to DaVinci Resolve."""
        self._connect()
        return self.is_connected

    @property
    def is_connected(self) -> bool:
        """Check if connected to DaVinci Resolve."""
        return self._resolve is not None

    @property
    def resolve(self) -> Any:
        """Get the Resolve object, raising if not connected."""
        if not self._resolve:
            raise NotConnectedError()
        return self._resolve

    @property
    def project_manager(self) -> Any:
        """Get the Project Manager object."""
        pm = self.resolve.GetProjectManager()
        if not pm:
            raise NotConnectedError("Failed to get Project Manager")
        return pm

    @property
    def current_project(self) -> Any:
        """Get the current project, raising if none is open."""
        project = self.project_manager.GetCurrentProject()
        if not project:
            raise NoProjectError()
        return project

    @property
    def media_pool(self) -> Any:
        """Get the Media Pool of the current project."""
        mp = self.current_project.GetMediaPool()
        if not mp:
            raise NoMediaPoolError()
        return mp

    @property
    def current_timeline(self) -> Any:
        """Get the current timeline, raising if none is active."""
        timeline = self.current_project.GetCurrentTimeline()
        if not timeline:
            raise NoTimelineError()
        return timeline

    @property
    def media_storage(self) -> Any:
        """Get the Media Storage object."""
        return self.resolve.GetMediaStorage()

    @property
    def fusion(self) -> Any:
        """Get the Fusion object."""
        return self.resolve.Fusion()

    @property
    def gallery(self) -> Any:
        """Get the Gallery object from current project."""
        return self.current_project.GetGallery()

    # Utility methods

    def get_version(self) -> str:
        """Get Resolve version string."""
        return f"{self.resolve.GetProductName()} {self.resolve.GetVersionString()}"

    def get_current_page(self) -> str:
        """Get the currently active page."""
        return self.resolve.GetCurrentPage()

    def switch_page(self, page: str) -> bool:
        """Switch to a specific page."""
        valid_pages = [
            "media",
            "cut",
            "edit",
            "fusion",
            "color",
            "fairlight",
            "deliver",
        ]
        if page.lower() not in valid_pages:
            raise ValueError(f"Invalid page. Must be one of: {', '.join(valid_pages)}")
        return self.resolve.OpenPage(page.lower())

    def get_all_clips(self, folder=None) -> list:
        """Get all clips from media pool recursively."""
        if folder is None:
            folder = self.media_pool.GetRootFolder()

        clips = []
        folder_clips = folder.GetClipList()
        if folder_clips:
            clips.extend(folder_clips)

        for sub_folder in folder.GetSubFolderList() or []:
            clips.extend(self.get_all_clips(sub_folder))

        return clips

    def get_all_folders(self, folder=None) -> list:
        """Get all folders from media pool recursively."""
        if folder is None:
            folder = self.media_pool.GetRootFolder()

        folders = [folder]
        for sub_folder in folder.GetSubFolderList() or []:
            folders.extend(self.get_all_folders(sub_folder))

        return folders

    def find_clip_by_name(self, name: str) -> Optional[Any]:
        """Find a clip by name in the media pool."""
        for clip in self.get_all_clips():
            if clip.GetName() == name:
                return clip
        return None

    def find_folder_by_name(self, name: str) -> Optional[Any]:
        """Find a folder by name in the media pool."""
        if name.lower() in ("root", "master"):
            return self.media_pool.GetRootFolder()

        for folder in self.get_all_folders():
            if folder.GetName() == name:
                return folder
        return None

    def find_timeline_item_by_id(self, item_id: str) -> Optional[tuple]:
        """
        Find a timeline item by its unique ID.

        Returns: tuple of (item, track_type, track_index) or None
        """
        timeline = self.current_timeline

        for track_type in ["video", "audio", "subtitle"]:
            track_count = timeline.GetTrackCount(track_type)
            for track_idx in range(1, track_count + 1):
                items = timeline.GetItemListInTrack(track_type, track_idx)
                if items:
                    for item in items:
                        if str(item.GetUniqueId()) == item_id:
                            return (item, track_type, track_idx)
        return None

    def find_timeline_by_name(self, name: str) -> Optional[Any]:
        """Find a timeline by name."""
        project = self.current_project
        for i in range(1, project.GetTimelineCount() + 1):
            timeline = project.GetTimelineByIndex(i)
            if timeline and timeline.GetName() == name:
                return timeline
        return None


# Module-level singleton accessor
_connection: Optional[ResolveConnection] = None


def get_resolve() -> ResolveConnection:
    """Get the global ResolveConnection instance."""
    global _connection
    if _connection is None:
        _connection = ResolveConnection()
    return _connection
