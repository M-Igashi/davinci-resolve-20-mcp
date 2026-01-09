#!/usr/bin/env python3
"""
DaVinci Resolve MCP Server - Optimized Version

A high-performance server connecting to DaVinci Resolve via Model Context Protocol (MCP).
This version eliminates code duplication and uses a modular architecture.

Version: 2.0.0
"""

import logging
import os
import sys
from typing import Any, Dict, List

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("davinci-resolve-mcp")

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import MCP
from mcp.server.fastmcp import FastMCP

# Import core
from core import ResolveConnection, get_resolve

# Import tools
from tools import color_group, gallery, graph, media, project, timeline, timeline_item
from tools import resolve as resolve_tools

VERSION = "2.0.0"

# Create MCP server
mcp = FastMCP("DaVinciResolveMCP")

# Initialize connection
conn = get_resolve()
if conn.is_connected:
    logger.info(f"DaVinci Resolve MCP Server v{VERSION}")
    logger.info(f"Connected to: {conn.get_version()}")
else:
    logger.error("Failed to connect to DaVinci Resolve. Is it running?")


# ==================== Resources ====================


@mcp.resource("resolve://version")
def resource_version() -> str:
    """Get DaVinci Resolve version."""
    return resolve_tools.get_version()


@mcp.resource("resolve://current-page")
def resource_current_page() -> str:
    """Get current page."""
    return resolve_tools.get_current_page()


@mcp.resource("resolve://projects")
def resource_projects() -> List[str]:
    """List all projects."""
    return project.list_projects()


@mcp.resource("resolve://current-project")
def resource_current_project() -> str:
    """Get current project name."""
    return project.get_current_project_name()


@mcp.resource("resolve://project-settings")
def resource_project_settings() -> Dict[str, Any]:
    """Get all project settings."""
    return project.get_project_settings()


@mcp.resource("resolve://timelines")
def resource_timelines() -> List[str]:
    """List all timelines."""
    return timeline.list_timelines()


@mcp.resource("resolve://current-timeline")
def resource_current_timeline() -> Dict[str, Any]:
    """Get current timeline info."""
    return timeline.get_current_timeline_info()


@mcp.resource("resolve://timeline-items")
def resource_timeline_items() -> List[Dict[str, Any]]:
    """Get all items in current timeline."""
    return timeline.get_all_timeline_items()


@mcp.resource("resolve://media-pool-clips")
def resource_media_pool_clips() -> List[Dict[str, Any]]:
    """List clips in root media pool folder."""
    return media.list_clips()


@mcp.resource("resolve://media-pool-folders")
def resource_media_pool_folders() -> List[str]:
    """List folders in root media pool."""
    return media.list_folders()


@mcp.resource("resolve://gallery-albums")
def resource_gallery_albums() -> List[Dict[str, Any]]:
    """List gallery still albums."""
    return gallery.get_gallery_still_albums()


@mcp.resource("resolve://color-groups")
def resource_color_groups() -> List[Dict[str, Any]]:
    """List color groups."""
    return color_group.list_color_groups()


@mcp.resource("resolve://render-formats")
def resource_render_formats() -> Dict[str, str]:
    """Get available render formats."""
    return project.get_render_formats()


@mcp.resource("resolve://render-jobs")
def resource_render_jobs() -> List[Any]:
    """Get render job queue."""
    return project.get_render_jobs()


@mcp.resource("resolve://mounted-volumes")
def resource_mounted_volumes() -> List[str]:
    """Get mounted storage volumes."""
    return resolve_tools.get_mounted_volumes()


@mcp.resource("resolve://keyframe-mode")
def resource_keyframe_mode() -> Dict[str, Any]:
    """Get current keyframe mode."""
    return resolve_tools.get_keyframe_mode()


# ==================== Resolve Tools ====================


@mcp.tool()
def switch_page(page: str) -> str:
    """Switch to a page (media/cut/edit/fusion/color/fairlight/deliver)."""
    return resolve_tools.switch_page(page)


@mcp.tool()
def load_layout_preset(preset_name: str) -> str:
    """Load a UI layout preset."""
    return resolve_tools.load_layout_preset(preset_name)


@mcp.tool()
def save_layout_preset(preset_name: str) -> str:
    """Save current layout as preset."""
    return resolve_tools.save_layout_preset(preset_name)


@mcp.tool()
def set_keyframe_mode(mode: int) -> str:
    """Set keyframe mode (0=All, 1=Color, 2=Sizing)."""
    return resolve_tools.set_keyframe_mode(mode)


@mcp.tool()
def import_render_preset(preset_path: str) -> str:
    """Import render preset from file."""
    return resolve_tools.import_render_preset(preset_path)


@mcp.tool()
def export_render_preset(preset_name: str, export_path: str) -> str:
    """Export render preset to file."""
    return resolve_tools.export_render_preset(preset_name, export_path)


# ==================== Project Tools ====================


@mcp.tool()
def open_project(name: str) -> str:
    """Open a project by name."""
    return project.open_project(name)


@mcp.tool()
def create_project(name: str, media_path: str = None) -> str:
    """Create a new project."""
    return project.create_project(name, media_path)


@mcp.tool()
def save_project() -> str:
    """Save the current project."""
    return project.save_project()


@mcp.tool()
def close_project() -> str:
    """Close the current project."""
    return project.close_project()


@mcp.tool()
def delete_project(name: str) -> str:
    """Delete a project by name."""
    return project.delete_project(name)


@mcp.tool()
def archive_project(
    name: str,
    file_path: str,
    archive_src_media: bool = True,
    archive_render_cache: bool = True,
) -> str:
    """Archive a project to file."""
    return project.archive_project(
        name, file_path, archive_src_media, archive_render_cache
    )


@mcp.tool()
def set_project_setting(setting_name: str, setting_value: Any) -> str:
    """Set a project setting."""
    return project.set_project_setting(setting_name, setting_value)


@mcp.tool()
def set_render_format_and_codec(format: str, codec: str) -> str:
    """Set render format and codec."""
    return project.set_render_format_and_codec(format, codec)


@mcp.tool()
def add_to_render_queue() -> str:
    """Add current timeline to render queue."""
    return project.add_to_render_queue()


@mcp.tool()
def start_rendering(job_ids: List[str] = None) -> str:
    """Start rendering jobs."""
    return project.start_rendering(job_ids)


@mcp.tool()
def stop_rendering() -> str:
    """Stop current rendering."""
    return project.stop_rendering()


@mcp.tool()
def delete_all_render_jobs() -> str:
    """Clear render queue."""
    return project.delete_all_render_jobs()


@mcp.tool()
def add_color_group(group_name: str) -> str:
    """Create a new color group."""
    return project.add_color_group(group_name)


@mcp.tool()
def refresh_lut_list() -> str:
    """Refresh LUT list."""
    return project.refresh_lut_list()


# ==================== Timeline Tools ====================


@mcp.tool()
def create_timeline(name: str) -> str:
    """Create a new timeline."""
    return timeline.create_timeline(name)


@mcp.tool()
def set_current_timeline(name: str) -> str:
    """Switch to a timeline by name."""
    return timeline.set_current_timeline(name)


@mcp.tool()
def duplicate_timeline(new_name: str = None) -> str:
    """Duplicate current timeline."""
    return timeline.duplicate_timeline(new_name)


@mcp.tool()
def delete_timelines(names: List[str]) -> str:
    """Delete timelines by name."""
    return timeline.delete_timelines(names)


@mcp.tool()
def add_track(track_type: str, sub_type: str = None) -> str:
    """Add a track (video/audio/subtitle)."""
    return timeline.add_track(track_type, sub_type)


@mcp.tool()
def delete_track(track_type: str, track_index: int) -> str:
    """Delete a track."""
    return timeline.delete_track(track_type, track_index)


@mcp.tool()
def set_track_enabled(track_type: str, track_index: int, enabled: bool) -> str:
    """Enable/disable a track."""
    return timeline.set_track_enabled(track_type, track_index, enabled)


@mcp.tool()
def set_track_locked(track_type: str, track_index: int, locked: bool) -> str:
    """Lock/unlock a track."""
    return timeline.set_track_locked(track_type, track_index, locked)


@mcp.tool()
def add_marker(frame: int, color: str = "Blue", name: str = "", note: str = "") -> str:
    """Add a timeline marker."""
    return timeline.add_marker(frame, color, name, note)


@mcp.tool()
def delete_marker_at_frame(frame: int) -> str:
    """Delete marker at frame."""
    return timeline.delete_marker_at_frame(frame)


@mcp.tool()
def set_current_timecode(timecode: str) -> str:
    """Set playhead position."""
    return timeline.set_current_timecode(timecode)


@mcp.tool()
def create_subtitles_from_audio(language: str = None) -> str:
    """Create subtitles from audio."""
    return timeline.create_subtitles_from_audio(language)


@mcp.tool()
def detect_scene_cuts() -> str:
    """Detect scene cuts in timeline."""
    return timeline.detect_scene_cuts()


@mcp.tool()
def grab_still() -> str:
    """Grab still from current clip."""
    return timeline.grab_still()


@mcp.tool()
def insert_generator(generator_name: str) -> str:
    """Insert a generator."""
    return timeline.insert_generator(generator_name)


@mcp.tool()
def insert_title(title_name: str) -> str:
    """Insert a title."""
    return timeline.insert_title(title_name)


@mcp.tool()
def create_compound_clip(item_ids: List[str], name: str = None) -> str:
    """Create compound clip from items."""
    return timeline.create_compound_clip(item_ids, name)


@mcp.tool()
def create_fusion_clip(item_ids: List[str]) -> str:
    """Create Fusion clip from items."""
    return timeline.create_fusion_clip(item_ids)


# ==================== Timeline Item Tools ====================


@mcp.tool()
def set_item_property(item_id: str, property_key: str, property_value: Any) -> str:
    """Set timeline item property."""
    return timeline_item.set_item_property(item_id, property_key, property_value)


@mcp.tool()
def set_item_enabled(item_id: str, enabled: bool) -> str:
    """Enable/disable timeline item."""
    return timeline_item.set_item_enabled(item_id, enabled)


@mcp.tool()
def add_item_marker(
    item_id: str, frame: int, color: str = "Blue", name: str = ""
) -> str:
    """Add marker to timeline item."""
    return timeline_item.add_item_marker(item_id, frame, color, name)


@mcp.tool()
def add_fusion_comp(item_id: str) -> str:
    """Add Fusion composition to item."""
    return timeline_item.add_fusion_comp(item_id)


@mcp.tool()
def add_version(item_id: str, version_name: str, version_type: int = 0) -> str:
    """Add color version (0=local, 1=remote)."""
    return timeline_item.add_version(item_id, version_name, version_type)


@mcp.tool()
def load_version(item_id: str, version_name: str, version_type: int = 0) -> str:
    """Load color version."""
    return timeline_item.load_version(item_id, version_name, version_type)


@mcp.tool()
def create_magic_mask(item_id: str, mode: str = "F") -> str:
    """Create magic mask (F/B/BI)."""
    return timeline_item.create_magic_mask(item_id, mode)


@mcp.tool()
def stabilize(item_id: str) -> str:
    """Stabilize a clip."""
    return timeline_item.stabilize(item_id)


@mcp.tool()
def smart_reframe(item_id: str) -> str:
    """Apply Smart Reframe."""
    return timeline_item.smart_reframe(item_id)


@mcp.tool()
def copy_grades(source_item_id: str, target_item_ids: List[str]) -> str:
    """Copy grades between items."""
    return timeline_item.copy_grades(source_item_id, target_item_ids)


@mcp.tool()
def export_lut(item_id: str, file_path: str, export_type: int = 1) -> str:
    """Export LUT from item (0=17pt, 1=33pt, 2=65pt)."""
    return timeline_item.export_lut(item_id, file_path, export_type)


@mcp.tool()
def assign_to_color_group(item_id: str, group_name: str) -> str:
    """Assign item to color group."""
    return timeline_item.assign_to_color_group(item_id, group_name)


# ==================== Media Pool Tools ====================


@mcp.tool()
def import_media(file_paths: List[str]) -> str:
    """Import media files."""
    return media.import_media(file_paths)


@mcp.tool()
def delete_clips(clip_names: List[str]) -> str:
    """Delete clips from media pool."""
    return media.delete_clips(clip_names)


@mcp.tool()
def move_clips(clip_names: List[str], target_folder: str) -> str:
    """Move clips to folder."""
    return media.move_clips(clip_names, target_folder)


@mcp.tool()
def create_folder(folder_name: str, parent_folder: str = None) -> str:
    """Create media pool folder."""
    return media.create_folder(folder_name, parent_folder)


@mcp.tool()
def set_clip_property(clip_name: str, property_name: str, property_value: Any) -> str:
    """Set clip property."""
    return media.set_clip_property(clip_name, property_name, property_value)


@mcp.tool()
def set_clip_metadata(clip_name: str, metadata: Dict[str, str]) -> str:
    """Set clip metadata."""
    return media.set_clip_metadata(clip_name, metadata)


@mcp.tool()
def link_proxy_media(clip_name: str, proxy_path: str) -> str:
    """Link proxy media to clip."""
    return media.link_proxy_media(clip_name, proxy_path)


@mcp.tool()
def unlink_proxy_media(clip_name: str) -> str:
    """Unlink proxy from clip."""
    return media.unlink_proxy_media(clip_name)


@mcp.tool()
def replace_clip(clip_name: str, new_file_path: str) -> str:
    """Replace clip with new file."""
    return media.replace_clip(clip_name, new_file_path)


@mcp.tool()
def transcribe_clip(clip_name: str) -> str:
    """Transcribe clip audio."""
    return media.transcribe_clip(clip_name)


@mcp.tool()
def transcribe_folder(folder_name: str) -> str:
    """Transcribe all clips in folder."""
    return media.transcribe_folder(folder_name)


@mcp.tool()
def append_to_timeline(clip_names: List[str]) -> str:
    """Append clips to timeline."""
    return media.append_to_timeline(clip_names)


@mcp.tool()
def create_timeline_from_clips(timeline_name: str, clip_names: List[str]) -> str:
    """Create timeline from clips."""
    return media.create_timeline_from_clips(timeline_name, clip_names)


@mcp.tool()
def auto_sync_audio(clip_names: List[str], sync_mode: str = "timecode") -> str:
    """Sync audio between clips."""
    return media.auto_sync_audio(clip_names, sync_mode)


# ==================== Gallery Tools ====================


@mcp.tool()
def create_still_album() -> str:
    """Create a new gallery still album."""
    return gallery.create_still_album()


@mcp.tool()
def create_power_grade_album() -> str:
    """Create a new PowerGrade album."""
    return gallery.create_power_grade_album()


@mcp.tool()
def import_stills(album_name: str, file_paths: List[str]) -> str:
    """Import stills into album."""
    return gallery.import_stills(album_name, file_paths)


@mcp.tool()
def export_stills(
    album_name: str, still_indices: List[int], folder_path: str, format: str = "dpx"
) -> str:
    """Export stills from album."""
    return gallery.export_stills(
        album_name, still_indices, folder_path, "still", format
    )


# ==================== Graph Tools ====================


@mcp.tool()
def set_node_lut(item_id: str, node_index: int, lut_path: str) -> str:
    """Set LUT on node."""
    return graph.set_node_lut(item_id, node_index, lut_path)


@mcp.tool()
def set_node_enabled(item_id: str, node_index: int, enabled: bool) -> str:
    """Enable/disable node."""
    return graph.set_node_enabled(item_id, node_index, enabled)


@mcp.tool()
def reset_all_grades(item_id: str) -> str:
    """Reset all grades on item."""
    return graph.reset_all_grades(item_id)


@mcp.tool()
def apply_grade_from_drx(item_id: str, drx_path: str, grade_mode: int = 0) -> str:
    """Apply grade from DRX file."""
    return graph.apply_grade_from_drx(item_id, drx_path, grade_mode)


# ==================== Color Group Tools ====================


@mcp.tool()
def create_color_group(group_name: str) -> str:
    """Create a color group."""
    return color_group.create_color_group(group_name)


@mcp.tool()
def delete_color_group(group_name: str) -> str:
    """Delete a color group."""
    return color_group.delete_color_group(group_name)


@mcp.tool()
def set_pre_clip_lut(group_name: str, node_index: int, lut_path: str) -> str:
    """Set LUT on pre-clip node."""
    return color_group.set_pre_clip_lut(group_name, node_index, lut_path)


@mcp.tool()
def set_post_clip_lut(group_name: str, node_index: int, lut_path: str) -> str:
    """Set LUT on post-clip node."""
    return color_group.set_post_clip_lut(group_name, node_index, lut_path)


# ==================== Entry Point ====================


def main():
    """Main entry point."""
    if not conn.is_connected:
        logger.error("Cannot start server without connection to DaVinci Resolve")
        sys.exit(1)

    logger.info("Starting DaVinci Resolve MCP Server")
    mcp.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
