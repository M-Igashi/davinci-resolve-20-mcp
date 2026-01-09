"""
Project management tools for DaVinci Resolve MCP Server.

Covers: Project creation, opening, saving, settings, database management.
"""

from typing import Any, Dict, List

from ..core import handle_resolve_errors, require_project, require_resolve

# ==================== Project Operations ====================


@handle_resolve_errors
@require_resolve
def list_projects(conn=None) -> List[str]:
    """List all projects in the current folder."""
    pm = conn.project_manager
    projects = pm.GetProjectListInCurrentFolder()
    return [p for p in projects if p]


@handle_resolve_errors
@require_resolve
def get_current_project_name(conn=None) -> str:
    """Get the name of the currently open project."""
    try:
        return conn.current_project.GetName()
    except:
        return "No project currently open"


@handle_resolve_errors
@require_resolve
def open_project(name: str, conn=None) -> str:
    """Open a project by name."""
    if not name:
        return "Error: Project name cannot be empty"

    pm = conn.project_manager
    projects = pm.GetProjectListInCurrentFolder()

    if name not in projects:
        return f"Error: Project '{name}' not found. Available: {', '.join(projects)}"

    if pm.LoadProject(name):
        return f"Successfully opened project '{name}'"
    return f"Failed to open project '{name}'"


@handle_resolve_errors
@require_resolve
def create_project(name: str, media_path: str = None, conn=None) -> str:
    """Create a new project with optional media location path."""
    if not name:
        return "Error: Project name cannot be empty"

    pm = conn.project_manager
    projects = pm.GetProjectListInCurrentFolder()

    if name in projects:
        return f"Error: Project '{name}' already exists"

    if media_path:
        result = pm.CreateProject(name, media_path)
    else:
        result = pm.CreateProject(name)

    if result:
        return f"Successfully created project '{name}'"
    return f"Failed to create project '{name}'"


@handle_resolve_errors
@require_project
def save_project(conn=None, project=None) -> str:
    """Save the current project."""
    pm = conn.project_manager
    if pm.SaveProject():
        return f"Successfully saved project '{project.GetName()}'"
    return f"Project '{project.GetName()}' auto-save is likely active"


@handle_resolve_errors
@require_project
def close_project(conn=None, project=None) -> str:
    """Close the current project without saving."""
    name = project.GetName()
    pm = conn.project_manager
    if pm.CloseProject(project):
        return f"Successfully closed project '{name}'"
    return f"Failed to close project '{name}'"


@handle_resolve_errors
@require_resolve
def delete_project(name: str, conn=None) -> str:
    """Delete a project by name (must not be currently loaded)."""
    pm = conn.project_manager
    if pm.DeleteProject(name):
        return f"Successfully deleted project '{name}'"
    return f"Failed to delete project '{name}'"


@handle_resolve_errors
@require_resolve
def archive_project(
    name: str,
    file_path: str,
    archive_src_media: bool = True,
    archive_render_cache: bool = True,
    archive_proxy_media: bool = False,
    conn=None,
) -> str:
    """Archive a project to a file."""
    pm = conn.project_manager
    if pm.ArchiveProject(
        name, file_path, archive_src_media, archive_render_cache, archive_proxy_media
    ):
        return f"Successfully archived project '{name}' to '{file_path}'"
    return f"Failed to archive project '{name}'"


@handle_resolve_errors
@require_resolve
def import_project(file_path: str, project_name: str = None, conn=None) -> str:
    """Import a project from file."""
    pm = conn.project_manager
    if pm.ImportProject(file_path, project_name):
        return f"Successfully imported project from '{file_path}'"
    return f"Failed to import project from '{file_path}'"


@handle_resolve_errors
@require_resolve
def export_project(
    project_name: str, file_path: str, with_stills_and_luts: bool = True, conn=None
) -> str:
    """Export a project to file."""
    pm = conn.project_manager
    if pm.ExportProject(project_name, file_path, with_stills_and_luts):
        return f"Successfully exported project '{project_name}' to '{file_path}'"
    return f"Failed to export project '{project_name}'"


@handle_resolve_errors
@require_resolve
def restore_project(file_path: str, project_name: str = None, conn=None) -> str:
    """Restore a project from file."""
    pm = conn.project_manager
    if pm.RestoreProject(file_path, project_name):
        return f"Successfully restored project from '{file_path}'"
    return f"Failed to restore project from '{file_path}'"


# ==================== Project Settings ====================


@handle_resolve_errors
@require_project
def get_project_settings(conn=None, project=None) -> Dict[str, Any]:
    """Get all project settings."""
    return project.GetSetting("")


@handle_resolve_errors
@require_project
def get_project_setting(setting_name: str, conn=None, project=None) -> Dict[str, Any]:
    """Get a specific project setting."""
    value = project.GetSetting(setting_name)
    return {setting_name: value}


@handle_resolve_errors
@require_project
def set_project_setting(
    setting_name: str, setting_value: Any, conn=None, project=None
) -> str:
    """Set a project setting."""
    # Convert to appropriate type
    if isinstance(setting_value, str):
        if setting_value.isdigit():
            setting_value = int(setting_value)
        elif setting_value.replace(".", "", 1).replace("-", "", 1).isdigit():
            setting_value = float(setting_value)

    if project.SetSetting(setting_name, setting_value):
        return f"Successfully set '{setting_name}' to '{setting_value}'"
    return f"Failed to set '{setting_name}'"


# ==================== Database Management ====================


@handle_resolve_errors
@require_resolve
def get_current_database(conn=None) -> Dict[str, Any]:
    """Get current database connection info."""
    pm = conn.project_manager
    return pm.GetCurrentDatabase()


@handle_resolve_errors
@require_resolve
def get_database_list(conn=None) -> List[Dict[str, Any]]:
    """Get list of all configured databases."""
    pm = conn.project_manager
    return pm.GetDatabaseList()


@handle_resolve_errors
@require_resolve
def set_current_database(
    db_type: str, db_name: str, ip_address: str = "127.0.0.1", conn=None
) -> str:
    """Switch to a different database."""
    pm = conn.project_manager
    db_info = {
        "DbType": db_type,  # 'Disk' or 'PostgreSQL'
        "DbName": db_name,
        "IpAddress": ip_address,
    }
    if pm.SetCurrentDatabase(db_info):
        return f"Successfully switched to database '{db_name}'"
    return f"Failed to switch to database '{db_name}'"


# ==================== Folder Management ====================


@handle_resolve_errors
@require_resolve
def get_current_folder(conn=None) -> str:
    """Get current folder name in project manager."""
    pm = conn.project_manager
    return pm.GetCurrentFolder()


@handle_resolve_errors
@require_resolve
def get_folder_list(conn=None) -> List[str]:
    """Get list of folders in current location."""
    pm = conn.project_manager
    return pm.GetFolderListInCurrentFolder()


@handle_resolve_errors
@require_resolve
def create_folder(folder_name: str, conn=None) -> str:
    """Create a new folder in project manager."""
    pm = conn.project_manager
    if pm.CreateFolder(folder_name):
        return f"Successfully created folder '{folder_name}'"
    return f"Failed to create folder '{folder_name}'"


@handle_resolve_errors
@require_resolve
def delete_folder(folder_name: str, conn=None) -> str:
    """Delete a folder from project manager."""
    pm = conn.project_manager
    if pm.DeleteFolder(folder_name):
        return f"Successfully deleted folder '{folder_name}'"
    return f"Failed to delete folder '{folder_name}'"


@handle_resolve_errors
@require_resolve
def open_folder(folder_name: str, conn=None) -> str:
    """Open a folder in project manager."""
    pm = conn.project_manager
    if pm.OpenFolder(folder_name):
        return f"Successfully opened folder '{folder_name}'"
    return f"Failed to open folder '{folder_name}'"


@handle_resolve_errors
@require_resolve
def goto_root_folder(conn=None) -> str:
    """Navigate to root folder in project manager."""
    pm = conn.project_manager
    if pm.GotoRootFolder():
        return "Successfully navigated to root folder"
    return "Failed to navigate to root folder"


@handle_resolve_errors
@require_resolve
def goto_parent_folder(conn=None) -> str:
    """Navigate to parent folder in project manager."""
    pm = conn.project_manager
    if pm.GotoParentFolder():
        return "Successfully navigated to parent folder"
    return "Failed to navigate to parent folder"


# ==================== Render Operations ====================


@handle_resolve_errors
@require_project
def get_render_formats(conn=None, project=None) -> Dict[str, str]:
    """Get available render formats."""
    return project.GetRenderFormats()


@handle_resolve_errors
@require_project
def get_render_codecs(render_format: str, conn=None, project=None) -> Dict[str, str]:
    """Get available codecs for a render format."""
    return project.GetRenderCodecs(render_format)


@handle_resolve_errors
@require_project
def get_current_render_format_and_codec(conn=None, project=None) -> Dict[str, str]:
    """Get currently selected render format and codec."""
    return project.GetCurrentRenderFormatAndCodec()


@handle_resolve_errors
@require_project
def set_render_format_and_codec(
    format: str, codec: str, conn=None, project=None
) -> str:
    """Set render format and codec."""
    if project.SetCurrentRenderFormatAndCodec(format, codec):
        return f"Successfully set format to '{format}' with codec '{codec}'"
    return "Failed to set render format and codec"


@handle_resolve_errors
@require_project
def get_render_resolutions(
    format: str = None, codec: str = None, conn=None, project=None
) -> List[Dict[str, int]]:
    """Get available render resolutions for format/codec."""
    if format and codec:
        return project.GetRenderResolutions(format, codec)
    return project.GetRenderResolutions()


@handle_resolve_errors
@require_project
def get_render_presets(conn=None, project=None) -> List[Any]:
    """Get available render presets."""
    return project.GetRenderPresetList()


@handle_resolve_errors
@require_project
def load_render_preset(preset_name: str, conn=None, project=None) -> str:
    """Load a render preset."""
    if project.LoadRenderPreset(preset_name):
        return f"Successfully loaded render preset '{preset_name}'"
    return f"Failed to load render preset '{preset_name}'"


@handle_resolve_errors
@require_project
def save_render_preset(preset_name: str, conn=None, project=None) -> str:
    """Save current settings as a new render preset."""
    if project.SaveAsNewRenderPreset(preset_name):
        return f"Successfully saved render preset '{preset_name}'"
    return f"Failed to save render preset '{preset_name}'"


@handle_resolve_errors
@require_project
def delete_render_preset(preset_name: str, conn=None, project=None) -> str:
    """Delete a render preset."""
    if project.DeleteRenderPreset(preset_name):
        return f"Successfully deleted render preset '{preset_name}'"
    return f"Failed to delete render preset '{preset_name}'"


@handle_resolve_errors
@require_project
def set_render_settings(settings: Dict[str, Any], conn=None, project=None) -> str:
    """Set render settings from a dictionary."""
    if project.SetRenderSettings(settings):
        return "Successfully updated render settings"
    return "Failed to update render settings"


@handle_resolve_errors
@require_project
def add_to_render_queue(conn=None, project=None) -> str:
    """Add current timeline to render queue with current settings."""
    job_id = project.AddRenderJob()
    if job_id:
        return f"Added render job with ID: {job_id}"
    return "Failed to add render job"


@handle_resolve_errors
@require_project
def get_render_jobs(conn=None, project=None) -> List[Any]:
    """Get list of render jobs in queue."""
    return project.GetRenderJobList()


@handle_resolve_errors
@require_project
def get_render_job_status(job_id: str, conn=None, project=None) -> Dict[str, Any]:
    """Get status of a specific render job."""
    return project.GetRenderJobStatus(job_id)


@handle_resolve_errors
@require_project
def start_rendering(
    job_ids: List[str] = None, interactive: bool = False, conn=None, project=None
) -> str:
    """Start rendering jobs."""
    if job_ids:
        result = project.StartRendering(job_ids, interactive)
    else:
        result = project.StartRendering(interactive)

    if result:
        return "Rendering started"
    return "Failed to start rendering"


@handle_resolve_errors
@require_project
def stop_rendering(conn=None, project=None) -> str:
    """Stop any current render processes."""
    project.StopRendering()
    return "Rendering stopped"


@handle_resolve_errors
@require_project
def is_rendering_in_progress(conn=None, project=None) -> bool:
    """Check if rendering is currently in progress."""
    return project.IsRenderingInProgress()


@handle_resolve_errors
@require_project
def delete_render_job(job_id: str, conn=None, project=None) -> str:
    """Delete a render job from the queue."""
    if project.DeleteRenderJob(job_id):
        return f"Successfully deleted render job '{job_id}'"
    return f"Failed to delete render job '{job_id}'"


@handle_resolve_errors
@require_project
def delete_all_render_jobs(conn=None, project=None) -> str:
    """Delete all render jobs from the queue."""
    if project.DeleteAllRenderJobs():
        return "Successfully deleted all render jobs"
    return "Failed to delete render jobs"


@handle_resolve_errors
@require_project
def get_quick_export_presets(conn=None, project=None) -> List[str]:
    """Get list of Quick Export render presets."""
    return project.GetQuickExportRenderPresets()


@handle_resolve_errors
@require_project
def render_with_quick_export(
    preset_name: str,
    target_dir: str = None,
    custom_name: str = None,
    enable_upload: bool = False,
    conn=None,
    project=None,
) -> Dict[str, Any]:
    """Start quick export render for current timeline."""
    params = {}
    if target_dir:
        params["TargetDir"] = target_dir
    if custom_name:
        params["CustomName"] = custom_name
    if enable_upload:
        params["EnableUpload"] = enable_upload

    return project.RenderWithQuickExport(preset_name, params)


# ==================== Color Groups ====================


@handle_resolve_errors
@require_project
def get_color_groups(conn=None, project=None) -> List[Any]:
    """Get list of all color groups in the project."""
    return project.GetColorGroupsList()


@handle_resolve_errors
@require_project
def add_color_group(group_name: str, conn=None, project=None) -> str:
    """Create a new color group."""
    result = project.AddColorGroup(group_name)
    if result:
        return f"Successfully created color group '{group_name}'"
    return f"Failed to create color group '{group_name}'"


@handle_resolve_errors
@require_project
def delete_color_group(group_name: str, conn=None, project=None) -> str:
    """Delete a color group."""
    groups = project.GetColorGroupsList()
    target_group = None
    for g in groups:
        if g.GetName() == group_name:
            target_group = g
            break

    if not target_group:
        return f"Color group '{group_name}' not found"

    if project.DeleteColorGroup(target_group):
        return f"Successfully deleted color group '{group_name}'"
    return f"Failed to delete color group '{group_name}'"


# ==================== Misc Project Operations ====================


@handle_resolve_errors
@require_project
def refresh_lut_list(conn=None, project=None) -> str:
    """Refresh the LUT list."""
    if project.RefreshLUTList():
        return "Successfully refreshed LUT list"
    return "Failed to refresh LUT list"


@handle_resolve_errors
@require_project
def get_project_unique_id(conn=None, project=None) -> str:
    """Get unique ID for the project."""
    return project.GetUniqueId()


@handle_resolve_errors
@require_project
def export_current_frame_as_still(file_path: str, conn=None, project=None) -> str:
    """Export current frame as a still image."""
    if project.ExportCurrentFrameAsStill(file_path):
        return f"Successfully exported frame to '{file_path}'"
    return f"Failed to export frame to '{file_path}'"


@handle_resolve_errors
@require_project
def load_burn_in_preset(preset_name: str, conn=None, project=None) -> str:
    """Load a data burn-in preset."""
    if project.LoadBurnInPreset(preset_name):
        return f"Successfully loaded burn-in preset '{preset_name}'"
    return f"Failed to load burn-in preset '{preset_name}'"


@handle_resolve_errors
@require_project
def get_fairlight_presets(conn=None, project=None) -> List[str]:
    """Get list of Fairlight presets."""
    return conn.resolve.GetFairlightPresets()


@handle_resolve_errors
@require_project
def apply_fairlight_preset(preset_name: str, conn=None, project=None) -> str:
    """Apply a Fairlight preset to the current timeline."""
    if project.ApplyFairlightPresetToCurrentTimeline(preset_name):
        return f"Successfully applied Fairlight preset '{preset_name}'"
    return f"Failed to apply Fairlight preset '{preset_name}'"
