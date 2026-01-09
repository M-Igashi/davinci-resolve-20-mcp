# Changelog

All notable changes to the DaVinci Resolve MCP Server project will be documented in this file.

## [2.0.0] - 2025-01-09

### Major Architectural Refactor

This release represents a complete architectural overhaul focused on code quality, maintainability, and comprehensive API coverage.

### Added
- **Modular Architecture**: New `src/core/` and `src/tools/` directories with focused modules
- **ResolveConnection Singleton**: Centralized connection management in `src/core/connection.py`
- **Decorator Pattern**: `@require_resolve`, `@require_project`, `@require_timeline`, `@handle_resolve_errors` decorators eliminate boilerplate
- **Custom Exception Hierarchy**: `ResolveError`, `NotConnectedError`, `NoProjectError`, `NoTimelineError`, `NoMediaPoolError` in `src/core/errors.py`
- **314 API Functions**: Comprehensive coverage across 8 tool modules:
  - `project.py` (57 functions) - Project/database/folder/render management
  - `timeline.py` (60 functions) - Timeline CRUD, tracks, markers, AI features
  - `timeline_item.py` (64 functions) - Clip properties, fusion, versions, takes
  - `media.py` (57 functions) - Import/export, metadata, proxy, transcription
  - `gallery.py` (17 functions) - Still albums, power grades
  - `graph.py` (14 functions) - Node graph, LUTs, cache modes
  - `color_group.py` (16 functions) - Color group management
  - `resolve.py` (29 functions) - App control, layout presets, media storage
- **New Entry Point**: `src/server.py` as clean modular entry point
- **Full Type Hints**: Type annotations throughout codebase
- **October 2025 API**: Based on latest DaVinci Resolve Scripting API documentation

### Changed
- Reduced codebase from 4,600+ lines (single file) to ~2,500 lines across organized modules
- Eliminated 94x repeated `if resolve is None` checks via decorators
- Eliminated 69x repeated `GetProjectManager()` calls via singleton pattern
- Improved error messages with consistent exception handling

### Backward Compatibility
- Legacy `src/resolve_mcp_server.py` still works for existing configurations
- Same MCP tool interface - no client-side changes required

---

## [1.3.8] - 2025-04

### Improvements
- **Cursor Integration**: Added comprehensive documentation for Cursor setup process
- **Entry Point**: Standardized on `main.py` as the proper entry point
- **Configuration Templates**: Updated example configuration files to use correct paths
- **Documentation**: Added detailed troubleshooting for "client closed" errors in Cursor

### Fixed
- Ensured consistent documentation for environment setup

## [1.3.7] - 2025-03

### Improvements
- New one-step installation script for macOS/Linux and Windows
- Enhanced path resolution in scripts
- More reliable DaVinci Resolve detection
- Support for absolute paths in project and global configurations
- Added comprehensive verification tools for troubleshooting
- Improved error handling and feedback
- Enhanced documentation with detailed installation guide

### Fixed
- Configuration issues with project-level MCP configuration
- Updated documentation with detailed installation and troubleshooting steps

## [1.3.6] - 2025-03-29

### Added
- Comprehensive Feature Additions:
  - Complete MediaPoolItem functionality (LinkProxyMedia, UnlinkProxyMedia, ReplaceClip, TranscribeAudio, ClearTranscription)
  - Complete Folder object methods (Export, TranscribeAudio, ClearTranscription)
  - Cache Management implementation (cache mode, optimized media, proxy settings)
  - Timeline Item Properties implementation (transform, crop, composite, retime, stabilization, audio)
  - Keyframe Control implementation (add/modify/delete keyframes, interpolation control)
  - Color Preset Management implementation (save/apply/delete presets, album management)
  - LUT Export functionality (multiple formats, variable sizing, batch export)
  - Helper functions for recursively accessing media pool items

### Changed
- Project directory restructuring:
  - Moved documentation files to `docs/` directory
  - Moved test scripts to `scripts/tests/` directory
  - Moved configuration templates to `config-templates/` directory
  - Moved utility scripts to `scripts/` directory
- Updated Implementation Progress Summary to reflect 100% completion of MediaPoolItem and Folder features

## [1.3.5] - 2025-03-29

### Added
- Updated Cursor integration with new templating system
- Improved client-specific launcher scripts for better usability
- Added automatic Cursor MCP configuration generation
- Enhanced cross-platform compatibility in launcher scripts

### Changed
- Updated Cursor integration script to use project root relative paths
- Simplified launcher script by removing dependencies on intermediate scripts
- Improved virtual environment detection and validation

### Fixed
- Path handling in Cursor configuration for more reliable connections
- Virtual environment validation to prevent launch failures
- Environment variable checking with more robust validation

## [1.3.4] - 2025-03-28

### Changed
- Improved template configuration for MCP clients with better documentation
- Fixed Cursor integration templates to use direct Python path instead of MCP CLI
- Simplified configuration process by removing environment variable requirements
- Added clearer warnings in templates and README about path replacement
- Created VERSION.md file for easier version tracking

### Fixed
- Connection issues with Cursor MCP integration
- Path variable handling in configuration templates
- Configuration templates now use consistent variable naming

## [1.3.3] - 2025-03-27

### Fixed
- Improved Windows compatibility for the run-now.bat script:
  - Fixed ANSI color code syntax errors in Windows command prompt
  - Made the npm/Node.js check a warning instead of an error
  - Simplified environment variable handling for better Windows compatibility
  - Fixed command syntax in batch file for more reliable execution
  - Improved DaVinci Resolve process detection for Windows
  - Added support for detecting multiple possible DaVinci Resolve executable names
  - Enhanced batch file error handling and robustness
  - Fixed issue with running the MCP server executable on Windows
  - Increased timeout waiting for DaVinci Resolve to start
- Added Windows specific templates in config-templates

## [1.3.2] - 2025-03-28

### Added
- Experimental Windows support with platform-specific path detection
- Dynamic environment setup based on operating system
- Platform utility module for handling OS-specific paths and configurations
- Enhanced error messages with platform-specific environment setup instructions
- Windows pre-launch check script (PowerShell) with automatic environment configuration
- Windows batch file launcher for easy execution of the pre-launch check

### Changed
- Refactored path setup code to use platform detection
- Improved logging with platform-specific information
- Updated documentation to reflect Windows compatibility status
- Enhanced README with Windows-specific configuration instructions

### Fixed
- Platform-dependent path issues that prevented Windows compatibility
- Environment variable handling for cross-platform use
- Windows-specific configuration paths for Cursor integration

## [1.3.1] - 2025-03-27

### Added
- Universal launcher script (`mcp_resolve_launcher.sh`) for interactive and CLI interfaces
- Improved Claude Desktop integration script with better error handling
- Enhanced detection for running DaVinci Resolve process

### Changed
- Updated documentation to include new universal launcher functionality
- Improved server startup process with better error handling and logging
- Enhanced cross-client compatibility between Cursor and Claude Desktop

### Fixed
- Process detection issues when looking for running DaVinci Resolve
- Signal handling in server scripts for cleaner termination

## [1.3.0] - 2025-03-26

### Added
- Support for adding clips to timeline directly by name
- Intelligent marker placement with frame detection
- Enhanced logging and error reporting
- Improved code organization with modular architecture

### Changed
- Reorganized project structure for better maintainability
- Enhanced Claude Desktop integration with better error handling
- Optimized connection to DaVinci Resolve for faster response times
- Updated documentation to include more examples

### Fixed
- Issues with marker placement on empty timelines
- Media pool navigation in complex project structures
- Timing issues when rapidly sending commands to DaVinci Resolve

## [1.1.0] - 2025-03-26

### Added
- Claude Desktop integration with claude_desktop_config.json support
- Consolidated server management script (scripts/server.sh)
- Project structure reorganization for better maintenance
- Configuration templates for easier setup

### Changed
- Moved scripts to dedicated scripts/ directory
- Organized example files into examples/ directory
- Updated README with Claude Desktop instructions
- Updated FEATURES.md to reflect Claude Desktop compatibility

### Fixed
- Environment variable handling in server scripts
- Path references in documentation

## [1.0.0] - 2025-03-24

### Added
- Initial release with Cursor integration
- DaVinci Resolve connection functionality
- Project management features (list, open, create projects)
- Timeline operations (create, list, switch timelines)
- Marker functionality with advanced frame detection
- Media Pool operations (import media, create bins)
- Comprehensive setup scripts
- Pre-launch check script

### Changed
- Switched from original MCP framework to direct JSON-RPC for improved reliability

### Fixed
- Save Project functionality with multi-method approach
- Environment variable setup for consistent connection
