"""
Node Graph tools for DaVinci Resolve MCP Server.

Covers: Node graph manipulation, LUTs, cache modes.
"""

from typing import Any, Dict, List, Optional

from ..core import get_resolve, handle_resolve_errors, require_timeline


def _get_node_graph(conn, item_id: str = None, layer_idx: int = 1):
    """Get node graph from timeline item or timeline."""
    if item_id:
        result = conn.find_timeline_item_by_id(item_id)
        if not result:
            raise ValueError(f"Timeline item with ID '{item_id}' not found")
        item = result[0]
        return item.GetNodeGraph(layer_idx)
    else:
        timeline = conn.current_timeline
        return timeline.GetNodeGraph()


# ==================== Node Information ====================


@handle_resolve_errors
@require_timeline
def get_num_nodes(
    item_id: str = None, layer_idx: int = 1, conn=None, project=None, timeline=None
) -> int:
    """Get number of nodes in the graph."""
    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return 0
    return graph.GetNumNodes()


@handle_resolve_errors
@require_timeline
def get_node_label(
    item_id: str,
    node_index: int,
    layer_idx: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Get the label of a node."""
    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return "Error: Could not get node graph"
    return graph.GetNodeLabel(node_index)


@handle_resolve_errors
@require_timeline
def get_tools_in_node(
    item_id: str,
    node_index: int,
    layer_idx: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> List[str]:
    """Get list of tools used in a node."""
    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return []
    return graph.GetToolsInNode(node_index)


@handle_resolve_errors
@require_timeline
def set_node_enabled(
    item_id: str,
    node_index: int,
    enabled: bool,
    layer_idx: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Enable or disable a node."""
    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return "Error: Could not get node graph"

    if graph.SetNodeEnabled(node_index, enabled):
        state = "enabled" if enabled else "disabled"
        return f"Successfully {state} node {node_index}"
    return "Failed to change node state"


# ==================== LUT Operations ====================


@handle_resolve_errors
@require_timeline
def set_node_lut(
    item_id: str,
    node_index: int,
    lut_path: str,
    layer_idx: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Set LUT on a node."""
    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return "Error: Could not get node graph"

    if graph.SetLUT(node_index, lut_path):
        return f"Successfully set LUT on node {node_index}"
    return "Failed to set LUT"


@handle_resolve_errors
@require_timeline
def get_node_lut(
    item_id: str,
    node_index: int,
    layer_idx: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Get LUT path from a node."""
    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return "Error: Could not get node graph"
    return graph.GetLUT(node_index)


# ==================== Cache Mode ====================


@handle_resolve_errors
@require_timeline
def get_node_cache_mode(
    item_id: str,
    node_index: int,
    layer_idx: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> int:
    """Get cache mode for a node (-1=auto, 0=disabled, 1=enabled)."""
    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return -1
    return graph.GetNodeCacheMode(node_index)


@handle_resolve_errors
@require_timeline
def set_node_cache_mode(
    item_id: str,
    node_index: int,
    cache_value: int,
    layer_idx: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Set cache mode for a node (-1=auto, 0=disabled, 1=enabled)."""
    if cache_value not in [-1, 0, 1]:
        return "Error: cache_value must be -1 (auto), 0 (disabled), or 1 (enabled)"

    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return "Error: Could not get node graph"

    if graph.SetNodeCacheMode(node_index, cache_value):
        modes = {-1: "auto", 0: "disabled", 1: "enabled"}
        return f"Successfully set cache mode to {modes[cache_value]}"
    return "Failed to set cache mode"


# ==================== Grade Operations ====================


@handle_resolve_errors
@require_timeline
def apply_grade_from_drx(
    item_id: str,
    drx_path: str,
    grade_mode: int = 0,
    layer_idx: int = 1,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Apply grade from DRX file (0=no keyframes, 1=source timecode, 2=start frames)."""
    if grade_mode not in [0, 1, 2]:
        return "Error: grade_mode must be 0, 1, or 2"

    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return "Error: Could not get node graph"

    if graph.ApplyGradeFromDRX(drx_path, grade_mode):
        return "Successfully applied grade from DRX"
    return "Failed to apply grade"


@handle_resolve_errors
@require_timeline
def apply_arri_cdl_lut(
    item_id: str, layer_idx: int = 1, conn=None, project=None, timeline=None
) -> str:
    """Apply ARRI CDL and LUT."""
    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return "Error: Could not get node graph"

    if graph.ApplyArriCdlLut():
        return "Successfully applied ARRI CDL and LUT"
    return "Failed to apply ARRI CDL and LUT"


@handle_resolve_errors
@require_timeline
def reset_all_grades(
    item_id: str, layer_idx: int = 1, conn=None, project=None, timeline=None
) -> str:
    """Reset all grades in the node graph."""
    graph = _get_node_graph(conn, item_id, layer_idx)
    if not graph:
        return "Error: Could not get node graph"

    if graph.ResetAllGrades():
        return "Successfully reset all grades"
    return "Failed to reset grades"
