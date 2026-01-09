# DaVinci Resolve MCP Server

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/masahigashi/davinci-resolve-20-mcp/releases)
[![DaVinci Resolve](https://img.shields.io/badge/DaVinci%20Resolve-18.5+-darkred.svg)](https://www.blackmagicdesign.com/products/davinciresolve)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/macOS-stable-brightgreen.svg)](https://www.apple.com/macos/)
[![Windows](https://img.shields.io/badge/Windows-stable-brightgreen.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that connects AI coding assistants (Cursor, Claude Desktop, Claude Code) to DaVinci Resolve, enabling natural language control of video editing workflows.

## Acknowledgments

This project is a fork of [samuelgursky/davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp), created by **Samuel Gursky**. We extend our sincere gratitude for his pioneering work in bringing MCP integration to DaVinci Resolve. His original implementation laid the foundation for this project.

## What's New in v2.0.0

This release represents a major architectural overhaul focused on code quality, maintainability, and alignment with the latest DaVinci Resolve API (October 2025).

### Key Improvements

| Aspect | Before (v1.x) | After (v2.0.0) |
|--------|---------------|----------------|
| Architecture | Single 4,600+ line file | Modular structure (~2,500 lines across focused modules) |
| Code Duplication | 94x repeated connection checks | Zero duplication via decorators |
| API Coverage | Partial | Comprehensive (314 functions) |
| Type Safety | Minimal | Full type hints throughout |
| Error Handling | Inconsistent | Unified exception hierarchy |

### Architectural Changes

**New Modular Structure:**
```
src/
├── core/                    # Core infrastructure
│   ├── connection.py        # Singleton connection manager
│   ├── decorators.py        # @require_resolve, @require_project, etc.
│   └── errors.py            # Custom exception classes
├── tools/                   # MCP tool implementations
│   ├── project.py           # Project/database management (57 functions)
│   ├── timeline.py          # Timeline operations (60 functions)
│   ├── timeline_item.py     # Clip/item operations (64 functions)
│   ├── media.py             # Media pool operations (57 functions)
│   ├── gallery.py           # Gallery/stills (17 functions)
│   ├── graph.py             # Node graph operations (14 functions)
│   ├── color_group.py       # Color group management (16 functions)
│   └── resolve.py           # App-level operations (29 functions)
└── server.py                # New entry point (v2.0.0)
```

**Decorator Pattern:**
```python
# Before: Repeated boilerplate in every function
def some_tool():
    resolve = get_resolve_instance()
    if resolve is None:
        return "Error: DaVinci Resolve is not running"
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if project is None:
        return "Error: No project is currently open"
    # ... actual logic

# After: Clean, focused functions
@handle_resolve_errors
@require_project
def some_tool(*, conn, project):
    # Just the actual logic - decorators handle the rest
```

## Features

- **76 MCP Tools** - Comprehensive control over DaVinci Resolve
- **16 Resources** - Query project state, timelines, clips, and more
- **Full API Coverage** - Based on October 2025 Scripting API documentation
- **Cross-Platform** - macOS and Windows support

For a complete feature list, see [docs/FEATURES.md](docs/FEATURES.md).

## Requirements

- **macOS** or **Windows**
- **Python 3.10+**
- **DaVinci Resolve 18.5+** (Studio recommended for full API access)
- DaVinci Resolve running in the background

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/masahigashi/davinci-resolve-20-mcp.git
cd davinci-resolve-20-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

**macOS:**
```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

**Windows:**
```cmd
set RESOLVE_SCRIPT_API=C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting
set RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll
set PYTHONPATH=%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules
```

### Running the Server

```bash
# Using the new modular server (v2.0.0)
python src/server.py

# Or use the legacy server for compatibility
python src/resolve_mcp_server.py
```

## Configuration

### Claude Code / Claude Desktop

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/davinci-resolve-20-mcp/src/server.py"]
    }
  }
}
```

### Cursor

Create or edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/davinci-resolve-20-mcp/src/server.py"]
    }
  }
}
```

## Usage Examples

Once connected, you can control DaVinci Resolve with natural language:

- "What version of DaVinci Resolve is running?"
- "List all projects in the database"
- "Create a new timeline called 'Final Cut'"
- "Add a marker at the current playhead position"
- "Import all media from /path/to/footage"
- "Switch to the Color page"
- "Export the current frame as a still"

## Tool Categories

| Category | Description | Functions |
|----------|-------------|-----------|
| **Project** | Project/database/folder/render management | 57 |
| **Timeline** | Timeline CRUD, tracks, markers, AI features | 60 |
| **Timeline Item** | Clip properties, fusion, versions, takes, AI | 64 |
| **Media** | Import/export, metadata, proxy, transcription | 57 |
| **Gallery** | Still albums, power grades, import/export | 17 |
| **Graph** | Node graph, LUTs, cache modes | 14 |
| **Color Group** | Color group management, pre/post clip graphs | 16 |
| **Resolve** | App control, layout presets, media storage | 29 |

## Project Structure

```
davinci-resolve-20-mcp/
├── src/
│   ├── core/               # Core infrastructure (NEW)
│   ├── tools/              # Modular tool implementations (NEW)
│   ├── server.py           # New entry point v2.0.0 (NEW)
│   ├── resolve_mcp_server.py  # Legacy monolithic server
│   └── main.py             # Legacy entry point
├── docs/
│   ├── FEATURES.md         # Feature documentation
│   ├── CHANGELOG.md        # Version history
│   └── ...
├── config-templates/       # Configuration examples
├── scripts/                # Utility scripts
└── requirements.txt
```

## Migration from v1.x

The v2.0.0 release is backward compatible. You can:

1. **Use the new server** - Point your MCP config to `src/server.py`
2. **Keep using the legacy server** - `src/resolve_mcp_server.py` still works

The new modular architecture provides the same MCP interface with improved internal organization.

## Troubleshooting

### Connection Issues
- Ensure DaVinci Resolve is running before starting the server
- Verify environment variables are set correctly
- Check that Python paths point to your virtual environment

### API Errors
- Some features require DaVinci Resolve Studio (not the free version)
- Ensure you're using DaVinci Resolve 18.5 or later

### Logs
Check `scripts/cursor_resolve_server.log` for detailed error messages.

## Contributing

Contributions are welcome! The new modular architecture makes it easier to:

1. Add new tools - Create functions in the appropriate `src/tools/` module
2. Fix bugs - Each module is focused and testable
3. Improve documentation - Docstrings and type hints throughout

## License

MIT License - See [LICENSE](LICENSE) for details.

## Credits

- **Original Author**: [Samuel Gursky](https://github.com/samuelgursky) - Creator of the original davinci-resolve-mcp
- **Blackmagic Design** - For DaVinci Resolve and its comprehensive Scripting API
- **Anthropic** - For the Model Context Protocol specification

## Links

- [Original Repository](https://github.com/samuelgursky/davinci-resolve-mcp)
- [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve)
- [Model Context Protocol](https://modelcontextprotocol.io/)
