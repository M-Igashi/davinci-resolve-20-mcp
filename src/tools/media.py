"""
Media Pool tools for DaVinci Resolve MCP Server.

Covers: Media import, clips, folders, metadata, transcription.
"""

from typing import Any, Dict, List

from ..core import (
    handle_resolve_errors,
    require_media_pool,
    require_project,
)

# ==================== Media Import ====================


@handle_resolve_errors
@require_media_pool
def import_media(
    file_paths: List[str], conn=None, project=None, media_pool=None
) -> str:
    """Import media files into the current media pool folder."""
    results = media_pool.ImportMedia(file_paths)
    if results:
        return f"Successfully imported {len(results)} item(s)"
    return "Failed to import media"


@handle_resolve_errors
@require_media_pool
def import_media_with_options(
    clip_infos: List[Dict[str, Any]], conn=None, project=None, media_pool=None
) -> str:
    """Import media with specific options (FilePath, StartIndex, EndIndex)."""
    results = media_pool.ImportMedia(clip_infos)
    if results:
        return f"Successfully imported {len(results)} item(s)"
    return "Failed to import media"


@handle_resolve_errors
@require_project
def import_timeline_from_file(
    file_path: str,
    timeline_name: str = None,
    import_source_clips: bool = True,
    source_clips_path: str = None,
    conn=None,
    project=None,
) -> str:
    """Import timeline from AAF/EDL/XML/FCPXML/DRT/ADL/OTIO file."""
    media_pool = conn.media_pool
    options = {}
    if timeline_name:
        options["timelineName"] = timeline_name
    if not import_source_clips:
        options["importSourceClips"] = False
    if source_clips_path:
        options["sourceClipsPath"] = source_clips_path

    timeline = (
        media_pool.ImportTimelineFromFile(file_path, options)
        if options
        else media_pool.ImportTimelineFromFile(file_path)
    )
    if timeline:
        return f"Successfully imported timeline '{timeline.GetName()}'"
    return "Failed to import timeline"


@handle_resolve_errors
@require_media_pool
def import_folder_from_file(
    file_path: str,
    source_clips_path: str = "",
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Import folder from DRB file."""
    if media_pool.ImportFolderFromFile(file_path, source_clips_path):
        return f"Successfully imported folder from '{file_path}'"
    return "Failed to import folder"


# ==================== Clip Operations ====================


@handle_resolve_errors
@require_media_pool
def list_clips(
    folder_name: str = None, conn=None, project=None, media_pool=None
) -> List[Dict[str, Any]]:
    """List clips in a folder (or root if not specified)."""
    if folder_name:
        folder = conn.find_folder_by_name(folder_name)
        if not folder:
            return [{"error": f"Folder '{folder_name}' not found"}]
    else:
        folder = media_pool.GetRootFolder()

    clips = folder.GetClipList()
    if not clips:
        return []

    return [
        {
            "name": clip.GetName(),
            "id": clip.GetUniqueId(),
            "duration": clip.GetClipProperty("Duration"),
            "fps": clip.GetClipProperty("FPS"),
            "resolution": clip.GetClipProperty("Resolution"),
        }
        for clip in clips
    ]


@handle_resolve_errors
@require_media_pool
def get_clip_properties(
    clip_name: str, conn=None, project=None, media_pool=None
) -> Dict[str, Any]:
    """Get all properties of a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return {"error": f"Clip '{clip_name}' not found"}
    return clip.GetClipProperty()


@handle_resolve_errors
@require_media_pool
def get_clip_property(
    clip_name: str, property_name: str, conn=None, project=None, media_pool=None
) -> Any:
    """Get a specific property of a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"
    return clip.GetClipProperty(property_name)


@handle_resolve_errors
@require_media_pool
def set_clip_property(
    clip_name: str,
    property_name: str,
    property_value: Any,
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Set a clip property."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.SetClipProperty(property_name, property_value):
        return f"Successfully set '{property_name}' to '{property_value}'"
    return "Failed to set property"


@handle_resolve_errors
@require_media_pool
def delete_clips(
    clip_names: List[str], conn=None, project=None, media_pool=None
) -> str:
    """Delete clips from media pool."""
    clips_to_delete = []
    for name in clip_names:
        clip = conn.find_clip_by_name(name)
        if clip:
            clips_to_delete.append(clip)

    if not clips_to_delete:
        return "Error: No matching clips found"

    if media_pool.DeleteClips(clips_to_delete):
        return f"Successfully deleted {len(clips_to_delete)} clip(s)"
    return "Failed to delete clips"


@handle_resolve_errors
@require_media_pool
def move_clips(
    clip_names: List[str],
    target_folder_name: str,
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Move clips to a target folder."""
    clips = []
    for name in clip_names:
        clip = conn.find_clip_by_name(name)
        if clip:
            clips.append(clip)

    if not clips:
        return "Error: No matching clips found"

    target_folder = conn.find_folder_by_name(target_folder_name)
    if not target_folder:
        return f"Error: Folder '{target_folder_name}' not found"

    if media_pool.MoveClips(clips, target_folder):
        return f"Successfully moved {len(clips)} clip(s)"
    return "Failed to move clips"


@handle_resolve_errors
@require_media_pool
def get_selected_clips(
    conn=None, project=None, media_pool=None
) -> List[Dict[str, Any]]:
    """Get currently selected clips in media pool."""
    clips = media_pool.GetSelectedClips()
    if not clips:
        return []

    return [{"name": clip.GetName(), "id": clip.GetUniqueId()} for clip in clips]


@handle_resolve_errors
@require_media_pool
def set_selected_clip(clip_name: str, conn=None, project=None, media_pool=None) -> str:
    """Set the selected clip in media pool."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if media_pool.SetSelectedClip(clip):
        return f"Successfully selected clip '{clip_name}'"
    return "Failed to select clip"


# ==================== Folder Operations ====================


@handle_resolve_errors
@require_media_pool
def list_folders(
    parent_folder_name: str = None, conn=None, project=None, media_pool=None
) -> List[str]:
    """List subfolders in a folder (or root if not specified)."""
    if parent_folder_name:
        folder = conn.find_folder_by_name(parent_folder_name)
        if not folder:
            return [f"Error: Folder '{parent_folder_name}' not found"]
    else:
        folder = media_pool.GetRootFolder()

    subfolders = folder.GetSubFolderList()
    return [f.GetName() for f in subfolders] if subfolders else []


@handle_resolve_errors
@require_media_pool
def create_folder(
    folder_name: str,
    parent_folder_name: str = None,
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Create a new folder in media pool."""
    if parent_folder_name:
        parent = conn.find_folder_by_name(parent_folder_name)
        if not parent:
            return f"Error: Parent folder '{parent_folder_name}' not found"
    else:
        parent = media_pool.GetRootFolder()

    new_folder = media_pool.AddSubFolder(parent, folder_name)
    if new_folder:
        return f"Successfully created folder '{folder_name}'"
    return "Failed to create folder"


@handle_resolve_errors
@require_media_pool
def delete_folders(
    folder_names: List[str], conn=None, project=None, media_pool=None
) -> str:
    """Delete folders from media pool."""
    folders = []
    for name in folder_names:
        folder = conn.find_folder_by_name(name)
        if folder:
            folders.append(folder)

    if not folders:
        return "Error: No matching folders found"

    if media_pool.DeleteFolders(folders):
        return f"Successfully deleted {len(folders)} folder(s)"
    return "Failed to delete folders"


@handle_resolve_errors
@require_media_pool
def move_folders(
    folder_names: List[str],
    target_folder_name: str,
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Move folders to a target folder."""
    folders = []
    for name in folder_names:
        folder = conn.find_folder_by_name(name)
        if folder:
            folders.append(folder)

    if not folders:
        return "Error: No matching folders found"

    target = conn.find_folder_by_name(target_folder_name)
    if not target:
        return f"Error: Target folder '{target_folder_name}' not found"

    if media_pool.MoveFolders(folders, target):
        return f"Successfully moved {len(folders)} folder(s)"
    return "Failed to move folders"


@handle_resolve_errors
@require_media_pool
def get_current_folder(conn=None, project=None, media_pool=None) -> str:
    """Get currently selected folder in media pool."""
    folder = media_pool.GetCurrentFolder()
    return folder.GetName() if folder else "Root"


@handle_resolve_errors
@require_media_pool
def set_current_folder(
    folder_name: str, conn=None, project=None, media_pool=None
) -> str:
    """Set current folder in media pool."""
    folder = conn.find_folder_by_name(folder_name)
    if not folder:
        return f"Error: Folder '{folder_name}' not found"

    if media_pool.SetCurrentFolder(folder):
        return f"Successfully switched to folder '{folder_name}'"
    return "Failed to switch folder"


@handle_resolve_errors
@require_media_pool
def refresh_folders(conn=None, project=None, media_pool=None) -> str:
    """Refresh folders in collaboration mode."""
    if media_pool.RefreshFolders():
        return "Successfully refreshed folders"
    return "Failed to refresh folders"


@handle_resolve_errors
@require_media_pool
def export_folder(
    folder_name: str, file_path: str, conn=None, project=None, media_pool=None
) -> str:
    """Export folder to DRB file."""
    folder = conn.find_folder_by_name(folder_name)
    if not folder:
        return f"Error: Folder '{folder_name}' not found"

    if folder.Export(file_path):
        return f"Successfully exported folder to '{file_path}'"
    return "Failed to export folder"


# ==================== Metadata ====================


@handle_resolve_errors
@require_media_pool
def get_clip_metadata(
    clip_name: str, metadata_type: str = None, conn=None, project=None, media_pool=None
) -> Any:
    """Get clip metadata."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return {"error": f"Clip '{clip_name}' not found"}

    if metadata_type:
        return clip.GetMetadata(metadata_type)
    return clip.GetMetadata()


@handle_resolve_errors
@require_media_pool
def set_clip_metadata(
    clip_name: str, metadata: Dict[str, str], conn=None, project=None, media_pool=None
) -> str:
    """Set clip metadata."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.SetMetadata(metadata):
        return "Successfully set metadata"
    return "Failed to set metadata"


@handle_resolve_errors
@require_media_pool
def get_third_party_metadata(
    clip_name: str, metadata_type: str = None, conn=None, project=None, media_pool=None
) -> Any:
    """Get third-party metadata from clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return {"error": f"Clip '{clip_name}' not found"}

    if metadata_type:
        return clip.GetThirdPartyMetadata(metadata_type)
    return clip.GetThirdPartyMetadata()


@handle_resolve_errors
@require_media_pool
def set_third_party_metadata(
    clip_name: str, metadata: Dict[str, str], conn=None, project=None, media_pool=None
) -> str:
    """Set third-party metadata on clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.SetThirdPartyMetadata(metadata):
        return "Successfully set third-party metadata"
    return "Failed to set metadata"


@handle_resolve_errors
@require_media_pool
def export_metadata(
    file_name: str,
    clip_names: List[str] = None,
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Export metadata to CSV file."""
    clips = None
    if clip_names:
        clips = []
        for name in clip_names:
            clip = conn.find_clip_by_name(name)
            if clip:
                clips.append(clip)

    if media_pool.ExportMetadata(file_name, clips):
        return f"Successfully exported metadata to '{file_name}'"
    return "Failed to export metadata"


# ==================== Clip Name/Color/Flags ====================


@handle_resolve_errors
@require_media_pool
def set_clip_name(
    clip_name: str, new_name: str, conn=None, project=None, media_pool=None
) -> str:
    """Rename a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.SetName(new_name):
        return f"Successfully renamed to '{new_name}'"
    return "Failed to rename clip"


@handle_resolve_errors
@require_media_pool
def get_clip_color(clip_name: str, conn=None, project=None, media_pool=None) -> str:
    """Get clip color."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"
    return clip.GetClipColor()


@handle_resolve_errors
@require_media_pool
def set_clip_color(
    clip_name: str, color: str, conn=None, project=None, media_pool=None
) -> str:
    """Set clip color."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.SetClipColor(color):
        return f"Successfully set clip color to '{color}'"
    return "Failed to set clip color"


@handle_resolve_errors
@require_media_pool
def add_clip_flag(
    clip_name: str, color: str, conn=None, project=None, media_pool=None
) -> str:
    """Add a flag to a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.AddFlag(color):
        return f"Successfully added {color} flag"
    return "Failed to add flag"


@handle_resolve_errors
@require_media_pool
def get_clip_flags(
    clip_name: str, conn=None, project=None, media_pool=None
) -> List[str]:
    """Get all flags on a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return [f"Error: Clip '{clip_name}' not found"]
    return clip.GetFlagList()


@handle_resolve_errors
@require_media_pool
def clear_clip_flags(
    clip_name: str, color: str = "All", conn=None, project=None, media_pool=None
) -> str:
    """Clear flags from a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.ClearFlags(color):
        return f"Successfully cleared {color} flags"
    return "Failed to clear flags"


# ==================== Markers ====================


@handle_resolve_errors
@require_media_pool
def add_clip_marker(
    clip_name: str,
    frame: int,
    color: str = "Blue",
    name: str = "",
    note: str = "",
    duration: int = 1,
    custom_data: str = "",
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Add a marker to a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.AddMarker(frame, color, name, note, duration, custom_data):
        return f"Successfully added marker at frame {frame}"
    return "Failed to add marker"


@handle_resolve_errors
@require_media_pool
def get_clip_markers(
    clip_name: str, conn=None, project=None, media_pool=None
) -> Dict[int, Dict]:
    """Get all markers on a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return {"error": f"Clip '{clip_name}' not found"}
    return clip.GetMarkers()


@handle_resolve_errors
@require_media_pool
def delete_clip_marker(
    clip_name: str, frame: int, conn=None, project=None, media_pool=None
) -> str:
    """Delete a marker from a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.DeleteMarkerAtFrame(frame):
        return f"Successfully deleted marker at frame {frame}"
    return "Failed to delete marker"


# ==================== Proxy/Link Operations ====================


@handle_resolve_errors
@require_media_pool
def link_proxy_media(
    clip_name: str, proxy_path: str, conn=None, project=None, media_pool=None
) -> str:
    """Link proxy media to a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.LinkProxyMedia(proxy_path):
        return "Successfully linked proxy media"
    return "Failed to link proxy media"


@handle_resolve_errors
@require_media_pool
def link_full_res_media(
    clip_name: str, full_res_path: str, conn=None, project=None, media_pool=None
) -> str:
    """Link proxy to full resolution media."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.LinkFullResolutionMedia(full_res_path):
        return "Successfully linked full resolution media"
    return "Failed to link media"


@handle_resolve_errors
@require_media_pool
def unlink_proxy_media(clip_name: str, conn=None, project=None, media_pool=None) -> str:
    """Unlink proxy media from a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.UnlinkProxyMedia():
        return "Successfully unlinked proxy media"
    return "Failed to unlink proxy media"


@handle_resolve_errors
@require_media_pool
def replace_clip(
    clip_name: str,
    new_file_path: str,
    preserve_subclip: bool = False,
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Replace a clip with new media."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if preserve_subclip:
        result = clip.ReplaceClipPreserveSubClip(new_file_path)
    else:
        result = clip.ReplaceClip(new_file_path)

    if result:
        return f"Successfully replaced clip with '{new_file_path}'"
    return "Failed to replace clip"


@handle_resolve_errors
@require_media_pool
def relink_clips(
    clip_names: List[str], folder_path: str, conn=None, project=None, media_pool=None
) -> str:
    """Relink clips to a folder path."""
    clips = []
    for name in clip_names:
        clip = conn.find_clip_by_name(name)
        if clip:
            clips.append(clip)

    if not clips:
        return "Error: No matching clips found"

    if media_pool.RelinkClips(clips, folder_path):
        return f"Successfully relinked {len(clips)} clip(s)"
    return "Failed to relink clips"


@handle_resolve_errors
@require_media_pool
def unlink_clips(
    clip_names: List[str], conn=None, project=None, media_pool=None
) -> str:
    """Unlink clips from their media files."""
    clips = []
    for name in clip_names:
        clip = conn.find_clip_by_name(name)
        if clip:
            clips.append(clip)

    if not clips:
        return "Error: No matching clips found"

    if media_pool.UnlinkClips(clips):
        return f"Successfully unlinked {len(clips)} clip(s)"
    return "Failed to unlink clips"


# ==================== Transcription ====================


@handle_resolve_errors
@require_media_pool
def transcribe_clip(clip_name: str, conn=None, project=None, media_pool=None) -> str:
    """Transcribe audio of a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.TranscribeAudio():
        return "Successfully started audio transcription"
    return "Failed to start transcription"


@handle_resolve_errors
@require_media_pool
def clear_clip_transcription(
    clip_name: str, conn=None, project=None, media_pool=None
) -> str:
    """Clear transcription from a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.ClearTranscription():
        return "Successfully cleared transcription"
    return "Failed to clear transcription"


@handle_resolve_errors
@require_media_pool
def transcribe_folder(
    folder_name: str, conn=None, project=None, media_pool=None
) -> str:
    """Transcribe audio of all clips in a folder."""
    folder = conn.find_folder_by_name(folder_name)
    if not folder:
        return f"Error: Folder '{folder_name}' not found"

    if folder.TranscribeAudio():
        return "Successfully started folder transcription"
    return "Failed to start transcription"


@handle_resolve_errors
@require_media_pool
def clear_folder_transcription(
    folder_name: str, conn=None, project=None, media_pool=None
) -> str:
    """Clear transcription from all clips in a folder."""
    folder = conn.find_folder_by_name(folder_name)
    if not folder:
        return f"Error: Folder '{folder_name}' not found"

    if folder.ClearTranscription():
        return "Successfully cleared folder transcription"
    return "Failed to clear transcription"


# ==================== Timeline Operations ====================


@handle_resolve_errors
@require_media_pool
def append_to_timeline(
    clip_names: List[str], conn=None, project=None, media_pool=None
) -> str:
    """Append clips to the current timeline."""
    clips = []
    for name in clip_names:
        clip = conn.find_clip_by_name(name)
        if clip:
            clips.append(clip)

    if not clips:
        return "Error: No matching clips found"

    results = media_pool.AppendToTimeline(clips)
    if results:
        return f"Successfully appended {len(results)} clip(s) to timeline"
    return "Failed to append clips"


@handle_resolve_errors
@require_media_pool
def create_timeline_from_clips(
    timeline_name: str, clip_names: List[str], conn=None, project=None, media_pool=None
) -> str:
    """Create a new timeline from clips."""
    clips = []
    for name in clip_names:
        clip = conn.find_clip_by_name(name)
        if clip:
            clips.append(clip)

    if not clips:
        return "Error: No matching clips found"

    timeline = media_pool.CreateTimelineFromClips(timeline_name, clips)
    if timeline:
        return f"Successfully created timeline '{timeline_name}'"
    return "Failed to create timeline"


# ==================== Audio Sync ====================


@handle_resolve_errors
@require_media_pool
def auto_sync_audio(
    clip_names: List[str],
    sync_mode: str = "timecode",
    channel_number: int = 1,
    retain_embedded: bool = False,
    retain_video_metadata: bool = False,
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Sync audio between clips."""
    clips = []
    for name in clip_names:
        clip = conn.find_clip_by_name(name)
        if clip:
            clips.append(clip)

    if len(clips) < 2:
        return "Error: Need at least 2 clips (video and audio) for sync"

    # Note: Would need actual resolve enum values
    settings = {
        "channelNumber": channel_number,
        "retainEmbeddedAudio": retain_embedded,
        "retainVideoMetadata": retain_video_metadata,
    }

    if media_pool.AutoSyncAudio(clips, settings):
        return "Successfully synced audio"
    return "Failed to sync audio"


# ==================== Stereo ====================


@handle_resolve_errors
@require_media_pool
def create_stereo_clip(
    left_clip_name: str, right_clip_name: str, conn=None, project=None, media_pool=None
) -> str:
    """Create a stereo 3D clip from left/right clips."""
    left_clip = conn.find_clip_by_name(left_clip_name)
    right_clip = conn.find_clip_by_name(right_clip_name)

    if not left_clip:
        return f"Error: Left clip '{left_clip_name}' not found"
    if not right_clip:
        return f"Error: Right clip '{right_clip_name}' not found"

    result = media_pool.CreateStereoClip(left_clip, right_clip)
    if result:
        return "Successfully created stereo clip"
    return "Failed to create stereo clip"


# ==================== Mark In/Out ====================


@handle_resolve_errors
@require_media_pool
def get_clip_mark_in_out(
    clip_name: str, conn=None, project=None, media_pool=None
) -> Dict[str, Any]:
    """Get mark in/out for a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return {"error": f"Clip '{clip_name}' not found"}
    return clip.GetMarkInOut()


@handle_resolve_errors
@require_media_pool
def set_clip_mark_in_out(
    clip_name: str,
    mark_in: int,
    mark_out: int,
    mark_type: str = "all",
    conn=None,
    project=None,
    media_pool=None,
) -> str:
    """Set mark in/out for a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.SetMarkInOut(mark_in, mark_out, mark_type):
        return "Successfully set mark in/out"
    return "Failed to set mark in/out"


@handle_resolve_errors
@require_media_pool
def clear_clip_mark_in_out(
    clip_name: str, mark_type: str = "all", conn=None, project=None, media_pool=None
) -> str:
    """Clear mark in/out for a clip."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.ClearMarkInOut(mark_type):
        return "Successfully cleared mark in/out"
    return "Failed to clear mark in/out"


# ==================== Growing Files ====================


@handle_resolve_errors
@require_media_pool
def monitor_growing_file(
    clip_name: str, conn=None, project=None, media_pool=None
) -> str:
    """Monitor a growing file (live recording)."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"

    if clip.MonitorGrowingFile():
        return "Successfully started monitoring growing file"
    return "Failed to monitor file"


# ==================== Audio Mapping ====================


@handle_resolve_errors
@require_media_pool
def get_audio_mapping(clip_name: str, conn=None, project=None, media_pool=None) -> str:
    """Get audio channel mapping as JSON string."""
    clip = conn.find_clip_by_name(clip_name)
    if not clip:
        return f"Error: Clip '{clip_name}' not found"
    return clip.GetAudioMapping()
