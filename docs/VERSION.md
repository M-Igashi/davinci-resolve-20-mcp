# DaVinci Resolve MCP Server

Current Version: 2.0.0

## Release Information

### 2.0.0 - Major Architectural Refactor (January 2025)

This release represents a complete architectural overhaul of the MCP server.

**Key Changes:**
- **Modular Architecture**: Restructured from single 4,600+ line file to organized modules
- **New Core Infrastructure**: `src/core/` with connection management, decorators, and error handling
- **Tool Modules**: 8 focused modules in `src/tools/` covering all API areas
- **314 Functions**: Comprehensive DaVinci Resolve API coverage
- **Decorator Pattern**: Eliminates boilerplate with `@require_resolve`, `@require_project`, etc.
- **Type Safety**: Full type hints throughout the codebase
- **October 2025 API**: Based on latest DaVinci Resolve Scripting API documentation

**New Structure:**
```
src/
├── core/           # Connection, decorators, errors
├── tools/          # 8 modular tool implementations
└── server.py       # New entry point (v2.0.0)
```

**Backward Compatible**: Legacy `resolve_mcp_server.py` still works.

---

### 1.3.8 Changes
- **Cursor Integration**: Added comprehensive documentation for Cursor setup process
- **Entry Point**: Standardized on `main.py` as the proper entry point
- **Configuration Templates**: Updated example configuration files to use correct paths

### 1.3.7 Changes
- Improved installation experience with one-step installation scripts
- Enhanced path resolution and DaVinci Resolve detection
- Added comprehensive verification tools for troubleshooting

### 1.3.6 Changes
- Complete MediaPoolItem and Folder object functionality
- Cache Management, Timeline Item Properties, Keyframe Control
- Color Preset Management, LUT Export functionality
- Project directory restructuring

### 1.3.5 Changes
- Updated Cursor integration with new templating system
- Improved client-specific launcher scripts
- Enhanced cross-platform compatibility

### 1.3.4 Changes
- Improved template configuration for MCP clients
- Fixed Cursor integration templates
- Simplified configuration process

## About

DaVinci Resolve MCP Server connects DaVinci Resolve to AI assistants through the Model Context Protocol, allowing AI agents to control DaVinci Resolve directly through natural language.

**Original Author**: Samuel Gursky ([samuelgursky/davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp))

For full changelog, see [CHANGELOG.md](CHANGELOG.md)
