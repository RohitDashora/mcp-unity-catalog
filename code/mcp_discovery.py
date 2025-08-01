#!/usr/bin/env python3
"""
MCP Tool Discovery Script

This script discovers all available tools from MCP servers and updates the mcp.json
configuration file with tool information, schemas, and descriptions.
"""

import json
import os
import sys
from typing import Dict, List, Any
from mcp_client import MCPClientManager


def discover_tools_for_server(client, server_name: str) -> Dict[str, Any]:
    """
    Discover all tools for a specific server and return their information.
    
    Args:
        client: MCPClient instance
        server_name: Name of the server
        
    Returns:
        Dictionary containing tool information
    """
    print(f"🔍 Discovering tools for server: {server_name}")
    
    try:
        if not client.initialize():
            print(f"❌ Failed to initialize client for {server_name}")
            return {}
        
        tools = client.list_tools()
        tool_info = {}
        
        for tool in tools:
            tool_info[tool.name] = {
                "description": tool.description,
                "input_schema": tool.input_schema,
                "server": server_name
            }
            print(f"  ✅ Found tool: {tool.name}")
        
        return tool_info
        
    except Exception as e:
        print(f"❌ Error discovering tools for {server_name}: {e}")
        return {}


def update_mcp_config(config_path: str, discovered_tools: Dict[str, Any]):
    """
    Update the mcp.json file with discovered tool information.
    
    Args:
        config_path: Path to mcp.json file
        discovered_tools: Dictionary of discovered tools
    """
    try:
        # Read existing config
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Add tools section if it doesn't exist
        if 'tools' not in config:
            config['tools'] = {}
        
        # Update with discovered tools
        for tool_name, tool_info in discovered_tools.items():
            config['tools'][tool_name] = tool_info
        
        # Write updated config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Updated {config_path} with {len(discovered_tools)} tools")
        
    except Exception as e:
        print(f"❌ Error updating config file: {e}")


def display_discovered_tools(tools: Dict[str, Any]):
    """
    Display discovered tools in a formatted way.
    
    Args:
        tools: Dictionary of discovered tools
    """
    if not tools:
        print("❌ No tools discovered")
        return
    
    print(f"\n📋 Discovered Tools ({len(tools)} total)")
    print("=" * 60)
    
    for tool_name, tool_info in tools.items():
        print(f"\n🔧 {tool_name}")
        print(f"   Server: {tool_info['server']}")
        print(f"   Description: {tool_info['description']}")
        
        if tool_info['input_schema']:
            print(f"   Input Schema:")
            schema_str = json.dumps(tool_info['input_schema'], indent=6)
            for line in schema_str.split('\n'):
                print(f"   {line}")
        
        print("-" * 40)


def discover_all_tools(config_path: str = ".cursor/mcp.json") -> Dict[str, Any]:
    """
    Discover all tools from all configured MCP servers.
    
    Args:
        config_path: Path to mcp.json configuration file
        
    Returns:
        Dictionary containing all discovered tools
    """
    print("🚀 MCP Tool Discovery")
    print("=" * 50)
    
    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        return {}
    
    try:
        # Create client manager
        manager = MCPClientManager(config_path)
        servers = manager.list_servers()
        
        if not servers:
            print("❌ No MCP servers found in configuration")
            return {}
        
        print(f"🌐 Found {len(servers)} MCP servers")
        all_tools = {}
        
        # Discover tools from each server
        for server_name in servers:
            client = manager.get_client(server_name)
            if client:
                server_tools = discover_tools_for_server(client, server_name)
                all_tools.update(server_tools)
        
        return all_tools
        
    except Exception as e:
        print(f"❌ Error during tool discovery: {e}")
        return {}


def main():
    """
    Main function for tool discovery.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Discover MCP tools and update configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Discover all tools and update mcp.json
  %(prog)s --display-only     # Discover tools but don't update config
  %(prog)s --config custom.json  # Use custom config file
        """
    )
    
    parser.add_argument(
        '--config',
        default='.cursor/mcp.json',
        help='Path to MCP configuration file (default: .cursor/mcp.json)'
    )
    
    parser.add_argument(
        '--display-only',
        action='store_true',
        help='Display discovered tools without updating configuration'
    )
    
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create backup of original config before updating'
    )
    
    args = parser.parse_args()
    
    # Create backup if requested
    if args.backup and os.path.exists(args.config):
        backup_path = f"{args.config}.backup"
        import shutil
        shutil.copy2(args.config, backup_path)
        print(f"📋 Created backup: {backup_path}")
    
    # Discover tools
    discovered_tools = discover_all_tools(args.config)
    
    if not discovered_tools:
        print("❌ No tools discovered")
        sys.exit(1)
    
    # Display discovered tools
    display_discovered_tools(discovered_tools)
    
    # Update configuration if not display-only
    if not args.display_only:
        update_mcp_config(args.config, discovered_tools)
        print(f"\n✅ Tool discovery complete! Updated {args.config}")
        print("💡 You can now use the tools with their full information in the config")
    else:
        print(f"\n✅ Tool discovery complete! (Display only mode)")


if __name__ == "__main__":
    main() 