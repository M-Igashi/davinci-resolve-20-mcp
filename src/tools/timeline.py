"""
Timeline management tools for DaVinci Resolve MCP Server.

Covers: Timeline creation, tracks, markers, clips, subtitles, and effects.
"""

from typing import Any, Dict, List, Optional

from ..core import (
    get_resolve,
    handle_resolve_errors,
    require_project,
    require_resolve,
    require_timeline,
)

# ==================== Timeline CRUD ====================


@handle_resolve_errors
@require_project
def list_timelines(conn=None, project=None) -> List[str]:
    """List all timelines in the current project."""
    timelines = []
    for i in range(1, project.GetTimelineCount() + 1):
        timeline = project.GetTimelineByIndex(i)
        if timeline:
            timelines.append(timeline.GetName())
    return timelines


@handle_resolve_errors
@require_timeline
def get_current_timeline_info(conn=None, project=None, timeline=None) -> Dict[str, Any]:
    """Get information about the current timeline."""
    return {
        "name": timeline.GetName(),
        "fps": timeline.GetSetting("timelineFrameRate"),
        "resolution": {
            "width": timeline.GetSetting("timelineResolutionWidth"),
            "height": timeline.GetSetting("timelineResolutionHeight"),
        },
        "start_frame": timeline.GetStartFrame(),
        "end_frame": timeline.GetEndFrame(),
        "duration": timeline.GetEndFrame() - timeline.GetStartFrame() + 1,
        "start_timecode": timeline.GetStartTimecode(),
        "unique_id": timeline.GetUniqueId(),
    }


@handle_resolve_errors
@require_project
def set_current_timeline(name: str, conn=None, project=None) -> str:
    """Switch to a timeline by name."""
    timeline = conn.find_timeline_by_name(name)
    if not timeline:
        return f"Error: Timeline '{name}' not found"

    if project.SetCurrentTimeline(timeline):
        return f"Successfully switched to timeline '{name}'"
    return f"Failed to switch to timeline '{name}'"


@handle_resolve_errors
@require_project
def create_timeline(name: str, conn=None, project=None) -> str:
    """Create a new empty timeline."""
    media_pool = conn.media_pool
    timeline = media_pool.CreateEmptyTimeline(name)
    if timeline:
        return f"Successfully created timeline '{name}'"
    return f"Failed to create timeline '{name}'"


@handle_resolve_errors
@require_timeline
def duplicate_timeline(
    new_name: str = None, conn=None, project=None, timeline=None
) -> str:
    """Duplicate the current timeline."""
    new_timeline = (
        timeline.DuplicateTimeline(new_name)
        if new_name
        else timeline.DuplicateTimeline()
    )
    if new_timeline:
        return f"Successfully duplicated timeline as '{new_timeline.GetName()}'"
    return "Failed to duplicate timeline"


@handle_resolve_errors
@require_project
def delete_timelines(names: List[str], conn=None, project=None) -> str:
    """Delete timelines by name."""
    media_pool = conn.media_pool
    timelines_to_delete = []

    for name in names:
        timeline = conn.find_timeline_by_name(name)
        if timeline:
            timelines_to_delete.append(timeline)

    if not timelines_to_delete:
        return "Error: No matching timelines found"

    if media_pool.DeleteTimelines(timelines_to_delete):
        return f"Successfully deleted {len(timelines_to_delete)} timeline(s)"
    return "Failed to delete timelines"


@handle_resolve_errors
@require_timeline
def set_timeline_name(new_name: str, conn=None, project=None, timeline=None) -> str:
    """Rename the current timeline."""
    old_name = timeline.GetName()
    if timeline.SetName(new_name):
        return f"Successfully renamed timeline from '{old_name}' to '{new_name}'"
    return f"Failed to rename timeline"


@handle_resolve_errors
@require_timeline
def set_start_timecode(timecode: str, conn=None, project=None, timeline=None) -> str:
    """Set the start timecode of the timeline."""
    if timeline.SetStartTimecode(timecode):
        return f"Successfully set start timecode to '{timecode}'"
    return f"Failed to set start timecode"


# ==================== Track Management ====================


@handle_resolve_errors
@require_timeline
def get_track_count(
    track_type: str = "video", conn=None, project=None, timeline=None
) -> int:
    """Get number of tracks of specified type."""
    valid_types = ["video", "audio", "subtitle"]
    if track_type not in valid_types:
        raise ValueError(f"Invalid track type. Must be one of: {valid_types}")
    return timeline.GetTrackCount(track_type)


@handle_resolve_errors
@require_timeline
def add_track(
    track_type: str,
    sub_type: str = None,
    index: int = None,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Add a new track to the timeline."""
    valid_types = ["video", "audio", "subtitle"]
    if track_type not in valid_types:
        return f"Error: Invalid track type. Must be one of: {valid_types}"

    if index is not None:
        options = {"index": index}
        if sub_type and track_type == "audio":
            options["audioType"] = sub_type
        result = timeline.AddTrack(track_type, options)
    elif sub_type and track_type == "audio":
        result = timeline.AddTrack(track_type, sub_type)
    else:
        result = timeline.AddTrack(track_type)

    if result:
        return f"Successfully added {track_type} track"
    return f"Failed to add {track_type} track"


@handle_resolve_errors
@require_timeline
def delete_track(
    track_type: str, track_index: int, conn=None, project=None, timeline=None
) -> str:
    """Delete a track from the timeline."""
    if timeline.DeleteTrack(track_type, track_index):
        return f"Successfully deleted {track_type} track {track_index}"
    return f"Failed to delete track"


@handle_resolve_errors
@require_timeline
def get_track_name(
    track_type: str, track_index: int, conn=None, project=None, timeline=None
) -> str:
    """Get the name of a track."""
    return timeline.GetTrackName(track_type, track_index)


@handle_resolve_errors
@require_timeline
def set_track_name(
    track_type: str, track_index: int, name: str, conn=None, project=None, timeline=None
) -> str:
    """Set the name of a track."""
    if timeline.SetTrackName(track_type, track_index, name):
        return f"Successfully renamed track to '{name}'"
    return "Failed to rename track"


@handle_resolve_errors
@require_timeline
def set_track_enabled(
    track_type: str,
    track_index: int,
    enabled: bool,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Enable or disable a track."""
    if timeline.SetTrackEnable(track_type, track_index, enabled):
        state = "enabled" if enabled else "disabled"
        return f"Successfully {state} {track_type} track {track_index}"
    return "Failed to change track state"


@handle_resolve_errors
@require_timeline
def is_track_enabled(
    track_type: str, track_index: int, conn=None, project=None, timeline=None
) -> bool:
    """Check if a track is enabled."""
    return timeline.GetIsTrackEnabled(track_type, track_index)


@handle_resolve_errors
@require_timeline
def set_track_locked(
    track_type: str,
    track_index: int,
    locked: bool,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Lock or unlock a track."""
    if timeline.SetTrackLock(track_type, track_index, locked):
        state = "locked" if locked else "unlocked"
        return f"Successfully {state} {track_type} track {track_index}"
    return "Failed to change track lock state"


@handle_resolve_errors
@require_timeline
def is_track_locked(
    track_type: str, track_index: int, conn=None, project=None, timeline=None
) -> bool:
    """Check if a track is locked."""
    return timeline.GetIsTrackLocked(track_type, track_index)


@handle_resolve_errors
@require_timeline
def get_track_sub_type(
    track_type: str, track_index: int, conn=None, project=None, timeline=None
) -> str:
    """Get the sub-type of a track (e.g., audio format)."""
    return timeline.GetTrackSubType(track_type, track_index)


# ==================== Timeline Items ====================


@handle_resolve_errors
@require_timeline
def get_items_in_track(
    track_type: str, track_index: int, conn=None, project=None, timeline=None
) -> List[Dict[str, Any]]:
    """Get all items in a specific track."""
    items = timeline.GetItemListInTrack(track_type, track_index)
    if not items:
        return []

    return [
        {
            "id": str(item.GetUniqueId()),
            "name": item.GetName(),
            "start_frame": item.GetStart(),
            "end_frame": item.GetEnd(),
            "duration": item.GetDuration(),
        }
        for item in items
    ]


@handle_resolve_errors
@require_timeline
def get_all_timeline_items(
    conn=None, project=None, timeline=None
) -> List[Dict[str, Any]]:
    """Get all items in the timeline across all tracks."""
    items = []

    for track_type in ["video", "audio", "subtitle"]:
        track_count = timeline.GetTrackCount(track_type)
        for track_idx in range(1, track_count + 1):
            track_items = timeline.GetItemListInTrack(track_type, track_idx)
            if track_items:
                for item in track_items:
                    items.append(
                        {
                            "id": str(item.GetUniqueId()),
                            "name": item.GetName(),
                            "type": track_type,
                            "track": track_idx,
                            "start_frame": item.GetStart(),
                            "end_frame": item.GetEnd(),
                            "duration": item.GetDuration(),
                        }
                    )

    return items


@handle_resolve_errors
@require_timeline
def get_current_video_item(conn=None, project=None, timeline=None) -> Dict[str, Any]:
    """Get the current video item at playhead."""
    item = timeline.GetCurrentVideoItem()
    if not item:
        return {"error": "No current video item"}

    return {
        "id": str(item.GetUniqueId()),
        "name": item.GetName(),
        "start_frame": item.GetStart(),
        "end_frame": item.GetEnd(),
        "duration": item.GetDuration(),
    }


@handle_resolve_errors
@require_timeline
def delete_clips(
    item_ids: List[str], ripple: bool = False, conn=None, project=None, timeline=None
) -> str:
    """Delete timeline items by ID."""
    items_to_delete = []
    for item_id in item_ids:
        result = conn.find_timeline_item_by_id(item_id)
        if result:
            items_to_delete.append(result[0])

    if not items_to_delete:
        return "Error: No matching items found"

    if timeline.DeleteClips(items_to_delete, ripple):
        return f"Successfully deleted {len(items_to_delete)} item(s)"
    return "Failed to delete items"


@handle_resolve_errors
@require_timeline
def set_clips_linked(
    item_ids: List[str], linked: bool, conn=None, project=None, timeline=None
) -> str:
    """Link or unlink timeline items."""
    items = []
    for item_id in item_ids:
        result = conn.find_timeline_item_by_id(item_id)
        if result:
            items.append(result[0])

    if not items:
        return "Error: No matching items found"

    if timeline.SetClipsLinked(items, linked):
        state = "linked" if linked else "unlinked"
        return f"Successfully {state} {len(items)} item(s)"
    return "Failed to change link state"


# ==================== Markers ====================


@handle_resolve_errors
@require_timeline
def add_marker(
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
    """Add a marker to the timeline."""
    valid_colors = [
        "Blue",
        "Cyan",
        "Green",
        "Yellow",
        "Red",
        "Pink",
        "Purple",
        "Fuchsia",
        "Rose",
        "Lavender",
        "Sky",
        "Mint",
        "Lemon",
        "Sand",
        "Cocoa",
        "Cream",
    ]

    if color not in valid_colors:
        return f"Error: Invalid color. Must be one of: {', '.join(valid_colors)}"

    if timeline.AddMarker(frame, color, name, note, duration, custom_data):
        return f"Successfully added {color} marker at frame {frame}"
    return "Failed to add marker"


@handle_resolve_errors
@require_timeline
def get_markers(conn=None, project=None, timeline=None) -> Dict[int, Dict[str, Any]]:
    """Get all markers on the timeline."""
    return timeline.GetMarkers()


@handle_resolve_errors
@require_timeline
def delete_marker_at_frame(frame: int, conn=None, project=None, timeline=None) -> str:
    """Delete marker at a specific frame."""
    if timeline.DeleteMarkerAtFrame(frame):
        return f"Successfully deleted marker at frame {frame}"
    return f"No marker found at frame {frame}"


@handle_resolve_errors
@require_timeline
def delete_markers_by_color(color: str, conn=None, project=None, timeline=None) -> str:
    """Delete all markers of a specific color."""
    if timeline.DeleteMarkersByColor(color):
        return f"Successfully deleted all {color} markers"
    return f"Failed to delete {color} markers"


@handle_resolve_errors
@require_timeline
def update_marker_custom_data(
    frame: int, custom_data: str, conn=None, project=None, timeline=None
) -> str:
    """Update custom data for a marker."""
    if timeline.UpdateMarkerCustomData(frame, custom_data):
        return f"Successfully updated marker custom data at frame {frame}"
    return "Failed to update marker custom data"


@handle_resolve_errors
@require_timeline
def get_marker_custom_data(frame: int, conn=None, project=None, timeline=None) -> str:
    """Get custom data for a marker at a frame."""
    return timeline.GetMarkerCustomData(frame)


# ==================== Playhead / Timecode ====================


@handle_resolve_errors
@require_timeline
def get_current_timecode(conn=None, project=None, timeline=None) -> str:
    """Get current playhead position as timecode."""
    return timeline.GetCurrentTimecode()


@handle_resolve_errors
@require_timeline
def set_current_timecode(timecode: str, conn=None, project=None, timeline=None) -> str:
    """Set current playhead position by timecode."""
    if timeline.SetCurrentTimecode(timecode):
        return f"Successfully set playhead to {timecode}"
    return f"Failed to set playhead to {timecode}"


# ==================== Subtitles ====================


@handle_resolve_errors
@require_timeline
def create_subtitles_from_audio(
    language: str = None,
    preset: str = None,
    chars_per_line: int = None,
    line_break: str = None,
    gap: int = None,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Create subtitles from audio using auto-captioning."""
    settings = {}

    # Note: These would need the actual resolve enum values
    # This is a simplified version
    if language:
        settings["language"] = language
    if preset:
        settings["preset"] = preset
    if chars_per_line:
        settings["charsPerLine"] = chars_per_line
    if gap is not None:
        settings["gap"] = gap

    if timeline.CreateSubtitlesFromAudio(settings):
        return "Successfully started subtitle creation from audio"
    return "Failed to create subtitles from audio"


# ==================== Scene Detection ====================


@handle_resolve_errors
@require_timeline
def detect_scene_cuts(conn=None, project=None, timeline=None) -> str:
    """Detect and create scene cuts along the timeline."""
    if timeline.DetectSceneCuts():
        return "Successfully detected scene cuts"
    return "Failed to detect scene cuts"


# ==================== Stereo ====================


@handle_resolve_errors
@require_timeline
def convert_to_stereo(conn=None, project=None, timeline=None) -> str:
    """Convert timeline to stereo."""
    if timeline.ConvertTimelineToStereo():
        return "Successfully converted timeline to stereo"
    return "Failed to convert to stereo"


# ==================== Dolby Vision ====================


@handle_resolve_errors
@require_timeline
def analyze_dolby_vision(
    item_ids: List[str] = None,
    blend_shots: bool = False,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Analyze Dolby Vision on timeline clips."""
    items = []
    if item_ids:
        for item_id in item_ids:
            result = conn.find_timeline_item_by_id(item_id)
            if result:
                items.append(result[0])

    # Note: Would need resolve.DLB_BLEND_SHOTS constant
    analysis_type = None  # or resolve.DLB_BLEND_SHOTS if blend_shots

    if timeline.AnalyzeDolbyVision(items, analysis_type):
        return "Successfully started Dolby Vision analysis"
    return "Failed to start Dolby Vision analysis"


# ==================== Voice Isolation ====================


@handle_resolve_errors
@require_timeline
def get_voice_isolation_state(
    track_index: int, conn=None, project=None, timeline=None
) -> Dict[str, Any]:
    """Get voice isolation state for an audio track."""
    return timeline.GetVoiceIsolationState(track_index)


@handle_resolve_errors
@require_timeline
def set_voice_isolation_state(
    track_index: int,
    enabled: bool,
    amount: int = 50,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Set voice isolation state for an audio track."""
    if amount < 0 or amount > 100:
        return "Error: Amount must be between 0 and 100"

    state = {"isEnabled": enabled, "amount": amount}
    if timeline.SetVoiceIsolationState(track_index, state):
        return f"Successfully set voice isolation for track {track_index}"
    return "Failed to set voice isolation"


# ==================== Compound/Fusion Clips ====================


@handle_resolve_errors
@require_timeline
def create_compound_clip(
    item_ids: List[str],
    name: str = None,
    start_timecode: str = None,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Create a compound clip from timeline items."""
    items = []
    for item_id in item_ids:
        result = conn.find_timeline_item_by_id(item_id)
        if result:
            items.append(result[0])

    if not items:
        return "Error: No matching items found"

    clip_info = {}
    if name:
        clip_info["name"] = name
    if start_timecode:
        clip_info["startTimecode"] = start_timecode

    result = (
        timeline.CreateCompoundClip(items, clip_info)
        if clip_info
        else timeline.CreateCompoundClip(items)
    )
    if result:
        return f"Successfully created compound clip"
    return "Failed to create compound clip"


@handle_resolve_errors
@require_timeline
def create_fusion_clip(
    item_ids: List[str], conn=None, project=None, timeline=None
) -> str:
    """Create a Fusion clip from timeline items."""
    items = []
    for item_id in item_ids:
        result = conn.find_timeline_item_by_id(item_id)
        if result:
            items.append(result[0])

    if not items:
        return "Error: No matching items found"

    result = timeline.CreateFusionClip(items)
    if result:
        return "Successfully created Fusion clip"
    return "Failed to create Fusion clip"


# ==================== Generators/Titles ====================


@handle_resolve_errors
@require_timeline
def insert_generator(
    generator_name: str, conn=None, project=None, timeline=None
) -> str:
    """Insert a generator into the timeline."""
    result = timeline.InsertGeneratorIntoTimeline(generator_name)
    if result:
        return f"Successfully inserted generator '{generator_name}'"
    return f"Failed to insert generator '{generator_name}'"


@handle_resolve_errors
@require_timeline
def insert_fusion_generator(
    generator_name: str, conn=None, project=None, timeline=None
) -> str:
    """Insert a Fusion generator into the timeline."""
    result = timeline.InsertFusionGeneratorIntoTimeline(generator_name)
    if result:
        return f"Successfully inserted Fusion generator '{generator_name}'"
    return f"Failed to insert Fusion generator '{generator_name}'"


@handle_resolve_errors
@require_timeline
def insert_title(title_name: str, conn=None, project=None, timeline=None) -> str:
    """Insert a title into the timeline."""
    result = timeline.InsertTitleIntoTimeline(title_name)
    if result:
        return f"Successfully inserted title '{title_name}'"
    return f"Failed to insert title '{title_name}'"


@handle_resolve_errors
@require_timeline
def insert_fusion_title(title_name: str, conn=None, project=None, timeline=None) -> str:
    """Insert a Fusion title into the timeline."""
    result = timeline.InsertFusionTitleIntoTimeline(title_name)
    if result:
        return f"Successfully inserted Fusion title '{title_name}'"
    return f"Failed to insert Fusion title '{title_name}'"


@handle_resolve_errors
@require_timeline
def insert_fusion_composition(conn=None, project=None, timeline=None) -> str:
    """Insert an empty Fusion composition into the timeline."""
    result = timeline.InsertFusionCompositionIntoTimeline()
    if result:
        return "Successfully inserted Fusion composition"
    return "Failed to insert Fusion composition"


@handle_resolve_errors
@require_timeline
def insert_ofx_generator(
    generator_name: str, conn=None, project=None, timeline=None
) -> str:
    """Insert an OFX generator into the timeline."""
    result = timeline.InsertOFXGeneratorIntoTimeline(generator_name)
    if result:
        return f"Successfully inserted OFX generator '{generator_name}'"
    return f"Failed to insert OFX generator '{generator_name}'"


# ==================== Gallery/Stills ====================


@handle_resolve_errors
@require_timeline
def grab_still(conn=None, project=None, timeline=None) -> str:
    """Grab a still from the current video clip."""
    result = timeline.GrabStill()
    if result:
        return "Successfully grabbed still"
    return "Failed to grab still"


@handle_resolve_errors
@require_timeline
def grab_all_stills(
    frame_source: int = 1, conn=None, project=None, timeline=None
) -> str:
    """Grab stills from all clips (1=first frame, 2=middle frame)."""
    if frame_source not in [1, 2]:
        return "Error: frame_source must be 1 (first) or 2 (middle)"

    results = timeline.GrabAllStills(frame_source)
    if results:
        return f"Successfully grabbed {len(results)} stills"
    return "Failed to grab stills"


# ==================== Export ====================


@handle_resolve_errors
@require_timeline
def export_timeline(
    file_name: str,
    export_type: str,
    export_subtype: str = None,
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Export the timeline to various formats."""
    # Note: Would need to map export_type/subtype strings to resolve constants
    # e.g., resolve.EXPORT_AAF, resolve.EXPORT_EDL, etc.

    if export_subtype:
        result = timeline.Export(file_name, export_type, export_subtype)
    else:
        result = timeline.Export(file_name, export_type, None)

    if result:
        return f"Successfully exported timeline to '{file_name}'"
    return "Failed to export timeline"


# ==================== Timeline Settings ====================


@handle_resolve_errors
@require_timeline
def get_timeline_setting(
    setting_name: str, conn=None, project=None, timeline=None
) -> Any:
    """Get a timeline setting value."""
    return timeline.GetSetting(setting_name)


@handle_resolve_errors
@require_timeline
def set_timeline_setting(
    setting_name: str, setting_value: Any, conn=None, project=None, timeline=None
) -> str:
    """Set a timeline setting value."""
    if timeline.SetSetting(setting_name, setting_value):
        return f"Successfully set '{setting_name}' to '{setting_value}'"
    return f"Failed to set timeline setting"


@handle_resolve_errors
@require_timeline
def get_all_timeline_settings(conn=None, project=None, timeline=None) -> Dict[str, Any]:
    """Get all timeline settings."""
    return timeline.GetSetting("")


# ==================== Mark In/Out ====================


@handle_resolve_errors
@require_timeline
def get_mark_in_out(conn=None, project=None, timeline=None) -> Dict[str, Any]:
    """Get timeline mark in/out points."""
    return timeline.GetMarkInOut()


@handle_resolve_errors
@require_timeline
def set_mark_in_out(
    mark_in: int,
    mark_out: int,
    mark_type: str = "all",
    conn=None,
    project=None,
    timeline=None,
) -> str:
    """Set timeline mark in/out points."""
    if mark_type not in ["video", "audio", "all"]:
        return "Error: mark_type must be 'video', 'audio', or 'all'"

    if timeline.SetMarkInOut(mark_in, mark_out, mark_type):
        return f"Successfully set mark in/out to {mark_in}/{mark_out}"
    return "Failed to set mark in/out"


@handle_resolve_errors
@require_timeline
def clear_mark_in_out(
    mark_type: str = "all", conn=None, project=None, timeline=None
) -> str:
    """Clear timeline mark in/out points."""
    if timeline.ClearMarkInOut(mark_type):
        return "Successfully cleared mark in/out"
    return "Failed to clear mark in/out"


# ==================== Thumbnail ====================


@handle_resolve_errors
@require_timeline
def get_current_clip_thumbnail(
    conn=None, project=None, timeline=None
) -> Dict[str, Any]:
    """Get thumbnail data for current clip in Color page."""
    return timeline.GetCurrentClipThumbnailImage()
