"""
Color Group tools for DaVinci Resolve MCP Server.

Covers: Color group management and pre/post clip node graphs.
"""

from typing import Any, Dict, List, Optional

from ..core import get_resolve, handle_resolve_errors, require_project, require_timeline


def _find_color_group(project, group_name: str):
    """Find a color group by name."""
    groups = project.GetColorGroupsList()
    for group in groups or []:
        if group.GetName() == group_name:
            return group
    return None


# ==================== Color Group CRUD ====================


@handle_resolve_errors
@require_project
def list_color_groups(conn=None, project=None) -> List[Dict[str, Any]]:
    """List all color groups in the project."""
    groups = project.GetColorGroupsList()
    if not groups:
        return []

    return [{"name": group.GetName()} for group in groups]


@handle_resolve_errors
@require_project
def create_color_group(group_name: str, conn=None, project=None) -> str:
    """Create a new color group."""
    result = project.AddColorGroup(group_name)
    if result:
        return f"Successfully created color group '{group_name}'"
    return f"Failed to create color group"


@handle_resolve_errors
@require_project
def delete_color_group(group_name: str, conn=None, project=None) -> str:
    """Delete a color group."""
    group = _find_color_group(project, group_name)
    if not group:
        return f"Error: Color group '{group_name}' not found"

    if project.DeleteColorGroup(group):
        return f"Successfully deleted color group '{group_name}'"
    return "Failed to delete color group"


@handle_resolve_errors
@require_project
def get_color_group_name(group_name: str, conn=None, project=None) -> str:
    """Get the name of a color group (for verification)."""
    group = _find_color_group(project, group_name)
    if not group:
        return f"Error: Color group '{group_name}' not found"
    return group.GetName()


@handle_resolve_errors
@require_project
def set_color_group_name(old_name: str, new_name: str, conn=None, project=None) -> str:
    """Rename a color group."""
    group = _find_color_group(project, old_name)
    if not group:
        return f"Error: Color group '{old_name}' not found"

    if group.SetName(new_name):
        return f"Successfully renamed to '{new_name}'"
    return "Failed to rename color group"


# ==================== Color Group Contents ====================


@handle_resolve_errors
@require_timeline
def get_clips_in_color_group(
    group_name: str, timeline_name: str = None, conn=None, project=None, timeline=None
) -> List[Dict[str, Any]]:
    """Get timeline items in a color group."""
    group = _find_color_group(project, group_name)
    if not group:
        return [{"error": f"Color group '{group_name}' not found"}]

    # Use specified timeline or current
    target_timeline = timeline
    if timeline_name:
        target_timeline = conn.find_timeline_by_name(timeline_name)
        if not target_timeline:
            return [{"error": f"Timeline '{timeline_name}' not found"}]

    clips = group.GetClipsInTimeline(target_timeline)
    if not clips:
        return []

    return [{"id": str(clip.GetUniqueId()), "name": clip.GetName()} for clip in clips]


# ==================== Pre/Post Clip Node Graphs ====================


@handle_resolve_errors
@require_project
def get_pre_clip_node_graph_info(
    group_name: str, conn=None, project=None
) -> Dict[str, Any]:
    """Get info about pre-clip node graph of a color group."""
    group = _find_color_group(project, group_name)
    if not group:
        return {"error": f"Color group '{group_name}' not found"}

    graph = group.GetPreClipNodeGraph()
    if not graph:
        return {"error": "No pre-clip node graph"}

    return {"num_nodes": graph.GetNumNodes()}


@handle_resolve_errors
@require_project
def get_post_clip_node_graph_info(
    group_name: str, conn=None, project=None
) -> Dict[str, Any]:
    """Get info about post-clip node graph of a color group."""
    group = _find_color_group(project, group_name)
    if not group:
        return {"error": f"Color group '{group_name}' not found"}

    graph = group.GetPostClipNodeGraph()
    if not graph:
        return {"error": "No post-clip node graph"}

    return {"num_nodes": graph.GetNumNodes()}


@handle_resolve_errors
@require_project
def set_pre_clip_lut(
    group_name: str, node_index: int, lut_path: str, conn=None, project=None
) -> str:
    """Set LUT on pre-clip node graph."""
    group = _find_color_group(project, group_name)
    if not group:
        return f"Error: Color group '{group_name}' not found"

    graph = group.GetPreClipNodeGraph()
    if not graph:
        return "Error: No pre-clip node graph"

    if graph.SetLUT(node_index, lut_path):
        return f"Successfully set LUT on pre-clip node {node_index}"
    return "Failed to set LUT"


@handle_resolve_errors
@require_project
def set_post_clip_lut(
    group_name: str, node_index: int, lut_path: str, conn=None, project=None
) -> str:
    """Set LUT on post-clip node graph."""
    group = _find_color_group(project, group_name)
    if not group:
        return f"Error: Color group '{group_name}' not found"

    graph = group.GetPostClipNodeGraph()
    if not graph:
        return "Error: No post-clip node graph"

    if graph.SetLUT(node_index, lut_path):
        return f"Successfully set LUT on post-clip node {node_index}"
    return "Failed to set LUT"


@handle_resolve_errors
@require_project
def reset_pre_clip_grades(group_name: str, conn=None, project=None) -> str:
    """Reset all grades in pre-clip node graph."""
    group = _find_color_group(project, group_name)
    if not group:
        return f"Error: Color group '{group_name}' not found"

    graph = group.GetPreClipNodeGraph()
    if not graph:
        return "Error: No pre-clip node graph"

    if graph.ResetAllGrades():
        return "Successfully reset pre-clip grades"
    return "Failed to reset grades"


@handle_resolve_errors
@require_project
def reset_post_clip_grades(group_name: str, conn=None, project=None) -> str:
    """Reset all grades in post-clip node graph."""
    group = _find_color_group(project, group_name)
    if not group:
        return f"Error: Color group '{group_name}' not found"

    graph = group.GetPostClipNodeGraph()
    if not graph:
        return "Error: No post-clip node graph"

    if graph.ResetAllGrades():
        return "Successfully reset post-clip grades"
    return "Failed to reset grades"
