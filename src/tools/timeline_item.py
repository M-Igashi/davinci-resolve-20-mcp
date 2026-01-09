"""
Timeline Item tools for DaVinci Resolve MCP Server.

Covers: Timeline item properties, transforms, effects, versions, Fusion, and AI features.
"""

from typing import Any, Dict, List, Optional

from ..core import get_resolve, handle_resolve_errors, require_timeline


def _get_item_by_id(conn, item_id: str):
    """Helper to get timeline item by ID."""
    result = conn.find_timeline_item_by_id(item_id)
    if not result:
        raise ValueError(f"Timeline item with ID '{item_id}' not found")
    return result[0]


# ==================== Basic Properties ====================


@handle_resolve_errors
@require_timeline
def get_item_properties(
    item_id: str, conn=None, project=None, timeline=None
) -> Dict[str, Any]:
    """Get all properties of a timeline item."""
    item = _get_item_by_id(conn, item_id)
    return item.GetProperty()


@handle_resolve_errors
@require_timeline
def get_item_property(
    item_id: str, property_key: str, conn=None, project=None, timeline=None
) -> Any:
    """Get a specific property of a timeline item."""
    item = _get_item_by_id(conn, item_id)
    return item.GetProperty(property_key)


@handle_resolve_errors
@require_timeline
def set_item_property(
    item_id: str,
    property_key: str,
    property_value: Any,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Set a property on a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.SetProperty(property_key, property_value):
        return f"Successfully set '{property_key}' to '{property_value}'"
    return f"Failed to set property '{property_key}'"


@handle_resolve_errors
@require_timeline
def set_item_properties(
    item_id: str, properties: Dict[str, Any], conn=None, project=None, timeline=None
) -> str:
    """Set multiple properties on a timeline item."""
    item = _get_item_by_id(conn, item_id)
    success_count = 0
    for key, value in properties.items():
        if item.SetProperty(key, value):
            success_count += 1
    return f"Successfully set {success_count}/{len(properties)} properties"


@handle_resolve_errors
@require_timeline
def get_item_name(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Get name of a timeline item."""
    item = _get_item_by_id(conn, item_id)
    return item.GetName()


@handle_resolve_errors
@require_timeline
def set_item_name(
    item_id: str, name: str, conn=None, project=None, timeline=None
) -> str:
    """Set name of a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.SetName(name):
        return f"Successfully renamed item to '{name}'"
    return "Failed to rename item"


@handle_resolve_errors
@require_timeline
def get_item_duration(
    item_id: str, subframe: bool = False, conn=None, project=None, timeline=None
) -> float:
    """Get duration of a timeline item."""
    item = _get_item_by_id(conn, item_id)
    return item.GetDuration(subframe)


@handle_resolve_errors
@require_timeline
def get_item_enabled(item_id: str, conn=None, project=None, timeline=None) -> bool:
    """Check if a timeline item is enabled."""
    item = _get_item_by_id(conn, item_id)
    return item.GetClipEnabled()


@handle_resolve_errors
@require_timeline
def set_item_enabled(
    item_id: str, enabled: bool, conn=None, project=None, timeline=None
) -> str:
    """Enable or disable a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.SetClipEnabled(enabled):
        state = "enabled" if enabled else "disabled"
        return f"Successfully {state} item"
    return "Failed to change item state"


# ==================== Clip Color/Flags ====================


@handle_resolve_errors
@require_timeline
def get_clip_color(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Get clip color of a timeline item."""
    item = _get_item_by_id(conn, item_id)
    return item.GetClipColor()


@handle_resolve_errors
@require_timeline
def set_clip_color(
    item_id: str, color: str, conn=None, project=None, timeline=None
) -> str:
    """Set clip color of a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.SetClipColor(color):
        return f"Successfully set clip color to '{color}'"
    return "Failed to set clip color"


@handle_resolve_errors
@require_timeline
def clear_clip_color(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Clear clip color of a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.ClearClipColor():
        return "Successfully cleared clip color"
    return "Failed to clear clip color"


@handle_resolve_errors
@require_timeline
def add_flag(item_id: str, color: str, conn=None, project=None, timeline=None) -> str:
    """Add a flag to a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.AddFlag(color):
        return f"Successfully added {color} flag"
    return f"Failed to add flag"


@handle_resolve_errors
@require_timeline
def get_flags(item_id: str, conn=None, project=None, timeline=None) -> List[str]:
    """Get all flags on a timeline item."""
    item = _get_item_by_id(conn, item_id)
    return item.GetFlagList()


@handle_resolve_errors
@require_timeline
def clear_flags(
    item_id: str, color: str = "All", conn=None, project=None, timeline=None
) -> str:
    """Clear flags from a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.ClearFlags(color):
        return f"Successfully cleared {color} flags"
    return "Failed to clear flags"


# ==================== Markers ====================


@handle_resolve_errors
@require_timeline
def add_item_marker(
    item_id: str,
    frame: int,
    color: str = "Blue",
    name: str = "",
    note: str = "",
    duration: int = 1,
    custom_data: str = "",
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Add a marker to a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.AddMarker(frame, color, name, note, duration, custom_data):
        return f"Successfully added marker at frame {frame}"
    return "Failed to add marker"


@handle_resolve_errors
@require_timeline
def get_item_markers(
    item_id: str, conn=None, project=None, timeline=None
) -> Dict[int, Dict]:
    """Get all markers on a timeline item."""
    item = _get_item_by_id(conn, item_id)
    return item.GetMarkers()


@handle_resolve_errors
@require_timeline
def delete_item_marker(
    item_id: str, frame: int, conn=None, project=None, timeline=None
) -> str:
    """Delete a marker from a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.DeleteMarkerAtFrame(frame):
        return f"Successfully deleted marker at frame {frame}"
    return "Failed to delete marker"


# ==================== Fusion Compositions ====================


@handle_resolve_errors
@require_timeline
def get_fusion_comp_count(item_id: str, conn=None, project=None, timeline=None) -> int:
    """Get number of Fusion compositions on a timeline item."""
    item = _get_item_by_id(conn, item_id)
    return item.GetFusionCompCount()


@handle_resolve_errors
@require_timeline
def get_fusion_comp_names(
    item_id: str, conn=None, project=None, timeline=None
) -> List[str]:
    """Get list of Fusion composition names."""
    item = _get_item_by_id(conn, item_id)
    return item.GetFusionCompNameList()


@handle_resolve_errors
@require_timeline
def add_fusion_comp(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Add a new Fusion composition to a timeline item."""
    item = _get_item_by_id(conn, item_id)
    result = item.AddFusionComp()
    if result:
        return "Successfully added Fusion composition"
    return "Failed to add Fusion composition"


@handle_resolve_errors
@require_timeline
def import_fusion_comp(
    item_id: str, file_path: str, conn=None, project=None, timeline=None
) -> str:
    """Import a Fusion composition from file."""
    item = _get_item_by_id(conn, item_id)
    result = item.ImportFusionComp(file_path)
    if result:
        return f"Successfully imported Fusion composition from '{file_path}'"
    return "Failed to import Fusion composition"


@handle_resolve_errors
@require_timeline
def export_fusion_comp(
    item_id: str,
    file_path: str,
    comp_index: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Export a Fusion composition to file."""
    item = _get_item_by_id(conn, item_id)
    if item.ExportFusionComp(file_path, comp_index):
        return f"Successfully exported Fusion composition to '{file_path}'"
    return "Failed to export Fusion composition"


@handle_resolve_errors
@require_timeline
def delete_fusion_comp(
    item_id: str, comp_name: str, conn=None, project=None, timeline=None
) -> str:
    """Delete a Fusion composition by name."""
    item = _get_item_by_id(conn, item_id)
    if item.DeleteFusionCompByName(comp_name):
        return f"Successfully deleted Fusion composition '{comp_name}'"
    return "Failed to delete Fusion composition"


@handle_resolve_errors
@require_timeline
def load_fusion_comp(
    item_id: str, comp_name: str, conn=None, project=None, timeline=None
) -> str:
    """Load a Fusion composition as active."""
    item = _get_item_by_id(conn, item_id)
    result = item.LoadFusionCompByName(comp_name)
    if result:
        return f"Successfully loaded Fusion composition '{comp_name}'"
    return "Failed to load Fusion composition"


@handle_resolve_errors
@require_timeline
def rename_fusion_comp(
    item_id: str, old_name: str, new_name: str, conn=None, project=None, timeline=None
) -> str:
    """Rename a Fusion composition."""
    item = _get_item_by_id(conn, item_id)
    if item.RenameFusionCompByName(old_name, new_name):
        return f"Successfully renamed Fusion composition to '{new_name}'"
    return "Failed to rename Fusion composition"


# ==================== Color Versions ====================


@handle_resolve_errors
@require_timeline
def add_version(
    item_id: str,
    version_name: str,
    version_type: int = 0,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Add a new color version (0=local, 1=remote)."""
    item = _get_item_by_id(conn, item_id)
    if item.AddVersion(version_name, version_type):
        vtype = "local" if version_type == 0 else "remote"
        return f"Successfully added {vtype} version '{version_name}'"
    return "Failed to add version"


@handle_resolve_errors
@require_timeline
def get_current_version(
    item_id: str, conn=None, project=None, timeline=None
) -> Dict[str, Any]:
    """Get current color version info."""
    item = _get_item_by_id(conn, item_id)
    return item.GetCurrentVersion()


@handle_resolve_errors
@require_timeline
def get_version_names(
    item_id: str, version_type: int = 0, conn=None, project=None, timeline=None
) -> List[str]:
    """Get list of version names (0=local, 1=remote)."""
    item = _get_item_by_id(conn, item_id)
    return item.GetVersionNameList(version_type)


@handle_resolve_errors
@require_timeline
def load_version(
    item_id: str,
    version_name: str,
    version_type: int = 0,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Load a color version."""
    item = _get_item_by_id(conn, item_id)
    if item.LoadVersionByName(version_name, version_type):
        return f"Successfully loaded version '{version_name}'"
    return "Failed to load version"


@handle_resolve_errors
@require_timeline
def delete_version(
    item_id: str,
    version_name: str,
    version_type: int = 0,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Delete a color version."""
    item = _get_item_by_id(conn, item_id)
    if item.DeleteVersionByName(version_name, version_type):
        return f"Successfully deleted version '{version_name}'"
    return "Failed to delete version"


@handle_resolve_errors
@require_timeline
def rename_version(
    item_id: str,
    old_name: str,
    new_name: str,
    version_type: int = 0,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Rename a color version."""
    item = _get_item_by_id(conn, item_id)
    if item.RenameVersionByName(old_name, new_name, version_type):
        return f"Successfully renamed version to '{new_name}'"
    return "Failed to rename version"


# ==================== Takes ====================


@handle_resolve_errors
@require_timeline
def add_take(
    item_id: str,
    media_pool_item_name: str,
    start_frame: int = None,
    end_frame: int = None,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Add a take to a timeline item."""
    item = _get_item_by_id(conn, item_id)
    mp_item = conn.find_clip_by_name(media_pool_item_name)
    if not mp_item:
        return f"Error: Media pool item '{media_pool_item_name}' not found"

    if start_frame is not None and end_frame is not None:
        result = item.AddTake(mp_item, start_frame, end_frame)
    else:
        result = item.AddTake(mp_item)

    if result:
        return "Successfully added take"
    return "Failed to add take"


@handle_resolve_errors
@require_timeline
def get_takes_count(item_id: str, conn=None, project=None, timeline=None) -> int:
    """Get number of takes in a take selector."""
    item = _get_item_by_id(conn, item_id)
    return item.GetTakesCount()


@handle_resolve_errors
@require_timeline
def get_selected_take_index(
    item_id: str, conn=None, project=None, timeline=None
) -> int:
    """Get currently selected take index."""
    item = _get_item_by_id(conn, item_id)
    return item.GetSelectedTakeIndex()


@handle_resolve_errors
@require_timeline
def select_take(
    item_id: str, take_index: int, conn=None, project=None, timeline=None
) -> str:
    """Select a take by index."""
    item = _get_item_by_id(conn, item_id)
    if item.SelectTakeByIndex(take_index):
        return f"Successfully selected take {take_index}"
    return "Failed to select take"


@handle_resolve_errors
@require_timeline
def delete_take(
    item_id: str, take_index: int, conn=None, project=None, timeline=None
) -> str:
    """Delete a take by index."""
    item = _get_item_by_id(conn, item_id)
    if item.DeleteTakeByIndex(take_index):
        return f"Successfully deleted take {take_index}"
    return "Failed to delete take"


@handle_resolve_errors
@require_timeline
def finalize_take(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Finalize take selection."""
    item = _get_item_by_id(conn, item_id)
    if item.FinalizeTake():
        return "Successfully finalized take"
    return "Failed to finalize take"


# ==================== AI Features ====================


@handle_resolve_errors
@require_timeline
def create_magic_mask(
    item_id: str, mode: str = "F", conn=None, project=None, timeline=None
) -> str:
    """Create magic mask (F=forward, B=backward, BI=bidirectional)."""
    if mode not in ["F", "B", "BI"]:
        return "Error: mode must be 'F', 'B', or 'BI'"

    item = _get_item_by_id(conn, item_id)
    if item.CreateMagicMask(mode):
        return "Successfully created magic mask"
    return "Failed to create magic mask"


@handle_resolve_errors
@require_timeline
def regenerate_magic_mask(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Regenerate magic mask."""
    item = _get_item_by_id(conn, item_id)
    if item.RegenerateMagicMask():
        return "Successfully regenerated magic mask"
    return "Failed to regenerate magic mask"


@handle_resolve_errors
@require_timeline
def stabilize(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Run stabilization on a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.Stabilize():
        return "Successfully stabilized clip"
    return "Failed to stabilize clip"


@handle_resolve_errors
@require_timeline
def smart_reframe(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Run Smart Reframe on a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.SmartReframe():
        return "Successfully applied Smart Reframe"
    return "Failed to apply Smart Reframe"


# ==================== Voice Isolation ====================


@handle_resolve_errors
@require_timeline
def get_item_voice_isolation(
    item_id: str, conn=None, project=None, timeline=None
) -> Dict[str, Any]:
    """Get voice isolation state for a timeline item."""
    item = _get_item_by_id(conn, item_id)
    return item.GetVoiceIsolationState()


@handle_resolve_errors
@require_timeline
def set_item_voice_isolation(
    item_id: str,
    enabled: bool,
    amount: int = 50,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Set voice isolation for a timeline item."""
    if amount < 0 or amount > 100:
        return "Error: amount must be between 0 and 100"

    item = _get_item_by_id(conn, item_id)
    state = {"isEnabled": enabled, "amount": amount}
    if item.SetVoiceIsolationState(state):
        return "Successfully set voice isolation"
    return "Failed to set voice isolation"


# ==================== Color Group ====================


@handle_resolve_errors
@require_timeline
def get_color_group(
    item_id: str, conn=None, project=None, timeline=None
) -> Optional[str]:
    """Get color group name for a timeline item."""
    item = _get_item_by_id(conn, item_id)
    group = item.GetColorGroup()
    return group.GetName() if group else None


@handle_resolve_errors
@require_timeline
def assign_to_color_group(
    item_id: str, group_name: str, conn=None, project=None, timeline=None
) -> str:
    """Assign timeline item to a color group."""
    item = _get_item_by_id(conn, item_id)

    # Find the color group
    groups = project.GetColorGroupsList()
    target_group = None
    for g in groups:
        if g.GetName() == group_name:
            target_group = g
            break

    if not target_group:
        return f"Error: Color group '{group_name}' not found"

    if item.AssignToColorGroup(target_group):
        return f"Successfully assigned to color group '{group_name}'"
    return "Failed to assign to color group"


@handle_resolve_errors
@require_timeline
def remove_from_color_group(
    item_id: str, conn=None, project=None, timeline=None
) -> str:
    """Remove timeline item from its color group."""
    item = _get_item_by_id(conn, item_id)
    if item.RemoveFromColorGroup():
        return "Successfully removed from color group"
    return "Failed to remove from color group"


# ==================== Grades/LUTs ====================


@handle_resolve_errors
@require_timeline
def copy_grades(
    source_item_id: str,
    target_item_ids: List[str],
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Copy grades from one item to others."""
    source = _get_item_by_id(conn, source_item_id)

    targets = []
    for tid in target_item_ids:
        try:
            targets.append(_get_item_by_id(conn, tid))
        except ValueError:
            pass

    if not targets:
        return "Error: No valid target items found"

    if source.CopyGrades(targets):
        return f"Successfully copied grades to {len(targets)} item(s)"
    return "Failed to copy grades"


@handle_resolve_errors
@require_timeline
def export_lut(
    item_id: str,
    file_path: str,
    export_type: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Export LUT from timeline item."""
    # export_type: 0=17pt, 1=33pt, 2=65pt, 3=Panasonic
    item = _get_item_by_id(conn, item_id)
    if item.ExportLUT(export_type, file_path):
        return f"Successfully exported LUT to '{file_path}'"
    return "Failed to export LUT"


@handle_resolve_errors
@require_timeline
def set_cdl(
    item_id: str,
    node_index: int,
    slope: str,
    offset: str,
    power: str,
    saturation: str,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Set CDL values on a node."""
    item = _get_item_by_id(conn, item_id)
    cdl_map = {
        "NodeIndex": str(node_index),
        "Slope": slope,
        "Offset": offset,
        "Power": power,
        "Saturation": saturation,
    }
    if item.SetCDL(cdl_map):
        return "Successfully set CDL values"
    return "Failed to set CDL values"


# ==================== Cache ====================


@handle_resolve_errors
@require_timeline
def get_color_cache_enabled(
    item_id: str, conn=None, project=None, timeline=None
) -> bool:
    """Check if color output cache is enabled."""
    item = _get_item_by_id(conn, item_id)
    return item.GetIsColorOutputCacheEnabled()


@handle_resolve_errors
@require_timeline
def set_color_cache(
    item_id: str, enabled: bool, conn=None, project=None, timeline=None
) -> str:
    """Set color output cache state."""
    item = _get_item_by_id(conn, item_id)
    if item.SetColorOutputCache(enabled):
        state = "enabled" if enabled else "disabled"
        return f"Successfully {state} color cache"
    return "Failed to set color cache"


@handle_resolve_errors
@require_timeline
def get_fusion_cache_enabled(
    item_id: str, conn=None, project=None, timeline=None
) -> Any:
    """Check Fusion output cache state."""
    item = _get_item_by_id(conn, item_id)
    return item.GetIsFusionOutputCacheEnabled()


@handle_resolve_errors
@require_timeline
def set_fusion_cache(
    item_id: str, cache_value: Any, conn=None, project=None, timeline=None
) -> str:
    """Set Fusion output cache state (auto, enabled, or disabled)."""
    item = _get_item_by_id(conn, item_id)
    if item.SetFusionOutputCache(cache_value):
        return "Successfully set Fusion cache"
    return "Failed to set Fusion cache"


# ==================== Misc ====================


@handle_resolve_errors
@require_timeline
def get_media_pool_item(
    item_id: str, conn=None, project=None, timeline=None
) -> Dict[str, Any]:
    """Get media pool item info for a timeline item."""
    item = _get_item_by_id(conn, item_id)
    mp_item = item.GetMediaPoolItem()
    if mp_item:
        return {"name": mp_item.GetName(), "id": mp_item.GetUniqueId()}
    return {"error": "No media pool item associated"}


@handle_resolve_errors
@require_timeline
def get_linked_items(item_id: str, conn=None, project=None, timeline=None) -> List[str]:
    """Get IDs of linked timeline items."""
    item = _get_item_by_id(conn, item_id)
    linked = item.GetLinkedItems()
    return [str(i.GetUniqueId()) for i in linked] if linked else []


@handle_resolve_errors
@require_timeline
def get_track_type_and_index(
    item_id: str, conn=None, project=None, timeline=None
) -> Dict[str, Any]:
    """Get track type and index for a timeline item."""
    item = _get_item_by_id(conn, item_id)
    result = item.GetTrackTypeAndIndex()
    return {"track_type": result[0], "track_index": result[1]}


@handle_resolve_errors
@require_timeline
def update_sidecar(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Update sidecar file for BRAW/R3D clips."""
    item = _get_item_by_id(conn, item_id)
    if item.UpdateSidecar():
        return "Successfully updated sidecar file"
    return "Failed to update sidecar file"


@handle_resolve_errors
@require_timeline
def load_burn_in_preset(
    item_id: str, preset_name: str, conn=None, project=None, timeline=None
) -> str:
    """Load a burn-in preset for a timeline item."""
    item = _get_item_by_id(conn, item_id)
    if item.LoadBurnInPreset(preset_name):
        return f"Successfully loaded burn-in preset '{preset_name}'"
    return "Failed to load burn-in preset"


@handle_resolve_errors
@require_timeline
def reset_all_node_colors(item_id: str, conn=None, project=None, timeline=None) -> str:
    """Reset node colors for all nodes in the active version."""
    item = _get_item_by_id(conn, item_id)
    if item.ResetAllNodeColors():
        return "Successfully reset all node colors"
    return "Failed to reset node colors"


@handle_resolve_errors
@require_timeline
def get_source_audio_mapping(
    item_id: str, conn=None, project=None, timeline=None
) -> str:
    """Get audio channel mapping as JSON string."""
    item = _get_item_by_id(conn, item_id)
    return item.GetSourceAudioChannelMapping()
