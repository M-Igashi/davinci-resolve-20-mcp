"""
Gallery tools for DaVinci Resolve MCP Server.

Covers: Gallery albums, stills, PowerGrades.
"""

from typing import Any, Dict, List, Optional

from ..core import get_resolve, handle_resolve_errors, require_project, with_page

# ==================== Album Operations ====================


@handle_resolve_errors
@require_project
def get_gallery_still_albums(conn=None, project=None) -> List[Dict[str, Any]]:
    """Get all gallery still albums."""
    gallery = conn.gallery
    albums = gallery.GetGalleryStillAlbums()
    if not albums:
        return []

    return [
        {
            "name": gallery.GetAlbumName(album),
            "still_count": len(album.GetStills()) if album.GetStills() else 0,
        }
        for album in albums
    ]


@handle_resolve_errors
@require_project
def get_power_grade_albums(conn=None, project=None) -> List[Dict[str, Any]]:
    """Get all PowerGrade albums."""
    gallery = conn.gallery
    albums = gallery.GetGalleryPowerGradeAlbums()
    if not albums:
        return []

    return [
        {
            "name": gallery.GetAlbumName(album),
            "still_count": len(album.GetStills()) if album.GetStills() else 0,
        }
        for album in albums
    ]


@handle_resolve_errors
@require_project
def get_current_still_album(conn=None, project=None) -> str:
    """Get the currently selected still album."""
    gallery = conn.gallery
    album = gallery.GetCurrentStillAlbum()
    return gallery.GetAlbumName(album) if album else None


@handle_resolve_errors
@require_project
def set_current_still_album(album_name: str, conn=None, project=None) -> str:
    """Set the current still album."""
    gallery = conn.gallery
    albums = gallery.GetGalleryStillAlbums()

    target_album = None
    for album in albums or []:
        if gallery.GetAlbumName(album) == album_name:
            target_album = album
            break

    if not target_album:
        return f"Error: Album '{album_name}' not found"

    if gallery.SetCurrentStillAlbum(target_album):
        return f"Successfully set current album to '{album_name}'"
    return "Failed to set current album"


@handle_resolve_errors
@require_project
def create_still_album(conn=None, project=None) -> str:
    """Create a new gallery still album."""
    gallery = conn.gallery
    album = gallery.CreateGalleryStillAlbum()
    if album:
        return f"Successfully created still album"
    return "Failed to create album"


@handle_resolve_errors
@require_project
def create_power_grade_album(conn=None, project=None) -> str:
    """Create a new PowerGrade album."""
    gallery = conn.gallery
    album = gallery.CreateGalleryPowerGradeAlbum()
    if album:
        return f"Successfully created PowerGrade album"
    return "Failed to create album"


@handle_resolve_errors
@require_project
def set_album_name(old_name: str, new_name: str, conn=None, project=None) -> str:
    """Rename a gallery album."""
    gallery = conn.gallery

    # Search in both still and PowerGrade albums
    all_albums = []
    still_albums = gallery.GetGalleryStillAlbums() or []
    power_albums = gallery.GetGalleryPowerGradeAlbums() or []
    all_albums.extend(still_albums)
    all_albums.extend(power_albums)

    target_album = None
    for album in all_albums:
        if gallery.GetAlbumName(album) == old_name:
            target_album = album
            break

    if not target_album:
        return f"Error: Album '{old_name}' not found"

    if gallery.SetAlbumName(target_album, new_name):
        return f"Successfully renamed album to '{new_name}'"
    return "Failed to rename album"


# ==================== Still Operations ====================


@handle_resolve_errors
@require_project
def get_stills_in_album(
    album_name: str = None, conn=None, project=None
) -> List[Dict[str, Any]]:
    """Get all stills in an album (current album if not specified)."""
    gallery = conn.gallery

    if album_name:
        # Find the album
        all_albums = []
        still_albums = gallery.GetGalleryStillAlbums() or []
        power_albums = gallery.GetGalleryPowerGradeAlbums() or []
        all_albums.extend(still_albums)
        all_albums.extend(power_albums)

        target_album = None
        for album in all_albums:
            if gallery.GetAlbumName(album) == album_name:
                target_album = album
                break

        if not target_album:
            return [{"error": f"Album '{album_name}' not found"}]
    else:
        target_album = gallery.GetCurrentStillAlbum()

    if not target_album:
        return [{"error": "No album available"}]

    stills = target_album.GetStills()
    if not stills:
        return []

    return [
        {"label": target_album.GetLabel(still), "index": idx}
        for idx, still in enumerate(stills)
    ]


@handle_resolve_errors
@require_project
def get_still_label(album_name: str, still_index: int, conn=None, project=None) -> str:
    """Get label for a specific still."""
    gallery = conn.gallery

    # Find the album
    all_albums = list(gallery.GetGalleryStillAlbums() or [])
    all_albums.extend(gallery.GetGalleryPowerGradeAlbums() or [])

    target_album = None
    for album in all_albums:
        if gallery.GetAlbumName(album) == album_name:
            target_album = album
            break

    if not target_album:
        return f"Error: Album '{album_name}' not found"

    stills = target_album.GetStills()
    if not stills or still_index >= len(stills):
        return "Error: Still not found"

    return target_album.GetLabel(stills[still_index])


@handle_resolve_errors
@require_project
def set_still_label(
    album_name: str, still_index: int, label: str, conn=None, project=None
) -> str:
    """Set label for a specific still."""
    gallery = conn.gallery

    all_albums = list(gallery.GetGalleryStillAlbums() or [])
    all_albums.extend(gallery.GetGalleryPowerGradeAlbums() or [])

    target_album = None
    for album in all_albums:
        if gallery.GetAlbumName(album) == album_name:
            target_album = album
            break

    if not target_album:
        return f"Error: Album '{album_name}' not found"

    stills = target_album.GetStills()
    if not stills or still_index >= len(stills):
        return "Error: Still not found"

    if target_album.SetLabel(stills[still_index], label):
        return f"Successfully set label to '{label}'"
    return "Failed to set label"


@handle_resolve_errors
@require_project
def import_stills(
    album_name: str, file_paths: List[str], conn=None, project=None
) -> str:
    """Import stills into an album."""
    gallery = conn.gallery

    all_albums = list(gallery.GetGalleryStillAlbums() or [])
    all_albums.extend(gallery.GetGalleryPowerGradeAlbums() or [])

    target_album = None
    for album in all_albums:
        if gallery.GetAlbumName(album) == album_name:
            target_album = album
            break

    if not target_album:
        return f"Error: Album '{album_name}' not found"

    if target_album.ImportStills(file_paths):
        return f"Successfully imported stills"
    return "Failed to import stills"


@handle_resolve_errors
@require_project
def export_stills(
    album_name: str,
    still_indices: List[int],
    folder_path: str,
    file_prefix: str = "still",
    format: str = "dpx",
    conn=None,
    project=None,
) -> str:
    """Export stills from an album."""
    gallery = conn.gallery

    all_albums = list(gallery.GetGalleryStillAlbums() or [])
    all_albums.extend(gallery.GetGalleryPowerGradeAlbums() or [])

    target_album = None
    for album in all_albums:
        if gallery.GetAlbumName(album) == album_name:
            target_album = album
            break

    if not target_album:
        return f"Error: Album '{album_name}' not found"

    stills = target_album.GetStills()
    if not stills:
        return "Error: No stills in album"

    stills_to_export = []
    for idx in still_indices:
        if idx < len(stills):
            stills_to_export.append(stills[idx])

    if not stills_to_export:
        return "Error: No valid still indices"

    valid_formats = ["dpx", "cin", "tif", "jpg", "png", "ppm", "bmp", "xpm", "drx"]
    if format.lower() not in valid_formats:
        return f"Error: Invalid format. Must be one of: {', '.join(valid_formats)}"

    if target_album.ExportStills(stills_to_export, folder_path, file_prefix, format):
        return f"Successfully exported {len(stills_to_export)} still(s)"
    return "Failed to export stills"


@handle_resolve_errors
@require_project
def delete_stills(
    album_name: str, still_indices: List[int], conn=None, project=None
) -> str:
    """Delete stills from an album."""
    gallery = conn.gallery

    all_albums = list(gallery.GetGalleryStillAlbums() or [])
    all_albums.extend(gallery.GetGalleryPowerGradeAlbums() or [])

    target_album = None
    for album in all_albums:
        if gallery.GetAlbumName(album) == album_name:
            target_album = album
            break

    if not target_album:
        return f"Error: Album '{album_name}' not found"

    stills = target_album.GetStills()
    if not stills:
        return "Error: No stills in album"

    stills_to_delete = []
    for idx in still_indices:
        if idx < len(stills):
            stills_to_delete.append(stills[idx])

    if not stills_to_delete:
        return "Error: No valid still indices"

    if target_album.DeleteStills(stills_to_delete):
        return f"Successfully deleted {len(stills_to_delete)} still(s)"
    return "Failed to delete stills"
