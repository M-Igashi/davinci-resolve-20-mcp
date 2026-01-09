"""
Resolve-level tools for DaVinci Resolve MCP Server.

Covers: App control, pages, presets, keyframe modes.
"""

from typing import Any, Dict, List, Optional

from ..core import get_resolve, handle_resolve_errors, require_resolve

# ==================== Application Control ====================


@handle_resolve_errors
@require_resolve
def get_version(conn=None) -> str:
    """Get DaVinci Resolve version string."""
    return conn.get_version()


@handle_resolve_errors
@require_resolve
def get_version_info(conn=None) -> Dict[str, Any]:
    """Get detailed version information."""
    resolve = conn.resolve
    version = resolve.GetVersion()
    return {
        "product": resolve.GetProductName(),
        "version_string": resolve.GetVersionString(),
        "major": version[0] if len(version) > 0 else None,
        "minor": version[1] if len(version) > 1 else None,
        "patch": version[2] if len(version) > 2 else None,
        "build": version[3] if len(version) > 3 else None,
        "suffix": version[4] if len(version) > 4 else None,
    }


@handle_resolve_errors
@require_resolve
def get_current_page(conn=None) -> str:
    """Get the currently active page."""
    return conn.get_current_page()


@handle_resolve_errors
@require_resolve
def switch_page(page: str, conn=None) -> str:
    """Switch to a specific page."""
    valid_pages = ["media", "cut", "edit", "fusion", "color", "fairlight", "deliver"]
    page = page.lower()

    if page not in valid_pages:
        return f"Error: Invalid page. Must be one of: {', '.join(valid_pages)}"

    if conn.switch_page(page):
        return f"Successfully switched to {page} page"
    return f"Failed to switch to {page} page"


@handle_resolve_errors
@require_resolve
def quit_resolve(conn=None) -> str:
    """Quit DaVinci Resolve application."""
    conn.resolve.Quit()
    return "DaVinci Resolve is quitting"


@handle_resolve_errors
@require_resolve
def get_fusion(conn=None) -> str:
    """Get Fusion object info."""
    fusion = conn.fusion
    if fusion:
        return "Fusion object available"
    return "Fusion object not available"


# ==================== Layout Presets ====================


@handle_resolve_errors
@require_resolve
def load_layout_preset(preset_name: str, conn=None) -> str:
    """Load a UI layout preset."""
    if conn.resolve.LoadLayoutPreset(preset_name):
        return f"Successfully loaded layout preset '{preset_name}'"
    return f"Failed to load layout preset '{preset_name}'"


@handle_resolve_errors
@require_resolve
def save_layout_preset(preset_name: str, conn=None) -> str:
    """Save current UI layout as a preset."""
    if conn.resolve.SaveLayoutPreset(preset_name):
        return f"Successfully saved layout preset '{preset_name}'"
    return f"Failed to save layout preset"


@handle_resolve_errors
@require_resolve
def update_layout_preset(preset_name: str, conn=None) -> str:
    """Update an existing layout preset with current layout."""
    if conn.resolve.UpdateLayoutPreset(preset_name):
        return f"Successfully updated layout preset '{preset_name}'"
    return f"Failed to update layout preset"


@handle_resolve_errors
@require_resolve
def delete_layout_preset(preset_name: str, conn=None) -> str:
    """Delete a layout preset."""
    if conn.resolve.DeleteLayoutPreset(preset_name):
        return f"Successfully deleted layout preset '{preset_name}'"
    return f"Failed to delete layout preset"


@handle_resolve_errors
@require_resolve
def export_layout_preset(preset_name: str, file_path: str, conn=None) -> str:
    """Export a layout preset to file."""
    if conn.resolve.ExportLayoutPreset(preset_name, file_path):
        return f"Successfully exported layout preset to '{file_path}'"
    return f"Failed to export layout preset"


@handle_resolve_errors
@require_resolve
def import_layout_preset(file_path: str, preset_name: str = None, conn=None) -> str:
    """Import a layout preset from file."""
    if preset_name:
        result = conn.resolve.ImportLayoutPreset(file_path, preset_name)
    else:
        result = conn.resolve.ImportLayoutPreset(file_path)

    if result:
        return f"Successfully imported layout preset from '{file_path}'"
    return f"Failed to import layout preset"


# ==================== Render/Burn-in Presets ====================


@handle_resolve_errors
@require_resolve
def import_render_preset(preset_path: str, conn=None) -> str:
    """Import a render preset from file and set as current."""
    if conn.resolve.ImportRenderPreset(preset_path):
        return f"Successfully imported render preset from '{preset_path}'"
    return f"Failed to import render preset"


@handle_resolve_errors
@require_resolve
def export_render_preset(preset_name: str, export_path: str, conn=None) -> str:
    """Export a render preset to file."""
    if conn.resolve.ExportRenderPreset(preset_name, export_path):
        return f"Successfully exported render preset to '{export_path}'"
    return f"Failed to export render preset"


@handle_resolve_errors
@require_resolve
def import_burn_in_preset(preset_path: str, conn=None) -> str:
    """Import a data burn-in preset from file."""
    if conn.resolve.ImportBurnInPreset(preset_path):
        return f"Successfully imported burn-in preset from '{preset_path}'"
    return f"Failed to import burn-in preset"


@handle_resolve_errors
@require_resolve
def export_burn_in_preset(preset_name: str, export_path: str, conn=None) -> str:
    """Export a data burn-in preset to file."""
    if conn.resolve.ExportBurnInPreset(preset_name, export_path):
        return f"Successfully exported burn-in preset to '{export_path}'"
    return f"Failed to export burn-in preset"


# ==================== Keyframe Mode ====================


@handle_resolve_errors
@require_resolve
def get_keyframe_mode(conn=None) -> Dict[str, Any]:
    """Get current keyframe mode."""
    mode = conn.resolve.GetKeyframeMode()
    mode_names = {0: "All", 1: "Color", 2: "Sizing"}
    return {"mode": mode, "name": mode_names.get(mode, "Unknown")}


@handle_resolve_errors
@require_resolve
def set_keyframe_mode(mode: int, conn=None) -> str:
    """Set keyframe mode (0=All, 1=Color, 2=Sizing)."""
    if mode not in [0, 1, 2]:
        return "Error: mode must be 0 (All), 1 (Color), or 2 (Sizing)"

    mode_names = {0: "All", 1: "Color", 2: "Sizing"}

    if conn.resolve.SetKeyframeMode(mode):
        return f"Successfully set keyframe mode to '{mode_names[mode]}'"
    return f"Failed to set keyframe mode"


# ==================== Media Storage ====================


@handle_resolve_errors
@require_resolve
def get_mounted_volumes(conn=None) -> List[str]:
    """Get list of mounted volumes in Media Storage."""
    storage = conn.media_storage
    return storage.GetMountedVolumeList()


@handle_resolve_errors
@require_resolve
def get_storage_subfolders(folder_path: str, conn=None) -> List[str]:
    """Get subfolders in a Media Storage path."""
    storage = conn.media_storage
    return storage.GetSubFolderList(folder_path)


@handle_resolve_errors
@require_resolve
def get_storage_files(folder_path: str, conn=None) -> List[str]:
    """Get files in a Media Storage path."""
    storage = conn.media_storage
    return storage.GetFileList(folder_path)


@handle_resolve_errors
@require_resolve
def reveal_in_storage(path: str, conn=None) -> str:
    """Reveal a path in Media Storage browser."""
    storage = conn.media_storage
    if storage.RevealInStorage(path):
        return f"Successfully revealed '{path}' in Media Storage"
    return f"Failed to reveal path"


@handle_resolve_errors
@require_resolve
def add_items_to_media_pool(paths: List[str], conn=None) -> str:
    """Add items from Media Storage to current Media Pool folder."""
    storage = conn.media_storage
    results = storage.AddItemListToMediaPool(paths)
    if results:
        return f"Successfully added {len(results)} item(s) to Media Pool"
    return "Failed to add items"


@handle_resolve_errors
@require_resolve
def add_clip_mattes(
    clip_name: str, matte_paths: List[str], stereo_eye: str = None, conn=None
) -> str:
    """Add mattes to a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    storage = conn.media_storage
    if stereo_eye:
        result = storage.AddClipMattesToMediaPool(clip, matte_paths, stereo_eye)
    else:
        result = storage.AddClipMattesToMediaPool(clip, matte_paths)

    if result:
        return "Successfully added clip mattes"
    return "Failed to add clip mattes"


@handle_resolve_errors
@require_resolve
def add_timeline_mattes(matte_paths: List[str], conn=None) -> str:
    """Add timeline mattes to current Media Pool folder."""
    storage = conn.media_storage
    results = storage.AddTimelineMattesToMediaPool(matte_paths)
    if results:
        return f"Successfully added {len(results)} timeline matte(s)"
    return "Failed to add timeline mattes"


# ==================== Fairlight Presets ====================


@handle_resolve_errors
@require_resolve
def get_fairlight_presets(conn=None) -> List[str]:
    """Get list of Fairlight presets."""
    return conn.resolve.GetFairlightPresets()
