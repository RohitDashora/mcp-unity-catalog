#!/usr/bin/env python3
"""
MCP CLI Tool

A command-line interface for interacting with Databricks MCP servers.
Provides easy access to tool discovery, schema viewing, and tool execution.
"""

import argparse
import sys
from mcp_client import MCPClientManager, display_results


def list_servers(manager: MCPClientManager):
    """List all available MCP servers."""
    manager.display_servers()


def list_tools(manager: MCPClientManager, server_name: str, detailed: bool = False):
    """List tools for a specific server."""
    client = manager.get_client(server_name)
    if not client:
        print(f"❌ Server '{server_name}' not found")
        return
    
    if not client.initialize():
        print(f"❌ Failed to initialize server '{server_name}'")
        return
    
    client.display_tools(detailed=detailed)


def show_tool_info(manager: MCPClientManager, server_name: str, tool_name: str):
    """Show detailed information about a specific tool."""
    client = manager.get_client(server_name)
    if not client:
        print(f"❌ Server '{server_name}' not found")
        return
    
    if not client.initialize():
        print(f"❌ Failed to initialize server '{server_name}'")
        return
    
    tool_info = client.get_tool_info(tool_name)
    if not tool_info:
        print(f"❌ Tool '{tool_name}' not found")
        return
    
    print(f"\n🔧 Tool Information")
    print("=" * 50)
    print(f"Name: {tool_info.name}")
    print(f"Description: {tool_info.description}")
    if tool_info.input_schema:
        print(f"Input Schema:")
        import json
        print(json.dumps(tool_info.input_schema, indent=2))


def search_wikipedia(manager: MCPClientManager, query: str):
    """Search Wikipedia using the vector search tool."""
    client = manager.get_client("wikipedia-search")
    if not client:
        print("❌ Wikipedia search server not found")
        return
    
    if not client.initialize():
        print("❌ Failed to initialize Wikipedia search server")
        return
    
    try:
        result = client.search_wikipedia(query)
        display_results(result)
    except Exception as e:
        print(f"❌ Search failed: {e}")


def call_tool(manager: MCPClientManager, server_name: str, tool_name: str, parameters: str):
    """Call a specific tool with parameters."""
    client = manager.get_client(server_name)
    if not client:
        print(f"❌ Server '{server_name}' not found")
        return
    
    if not client.initialize():
        print(f"❌ Failed to initialize server '{server_name}'")
        return
    
    try:
        import json
        params = json.loads(parameters)
        result = client.call_tool(tool_name, params)
        display_results(result)
    except json.JSONDecodeError:
        print("❌ Invalid JSON parameters")
    except Exception as e:
        print(f"❌ Tool call failed: {e}")


def interactive_mode(manager: MCPClientManager, server_name: str):
    """Start interactive mode for a specific server."""
    client = manager.get_client(server_name)
    if not client:
        print(f"❌ Server '{server_name}' not found")
        return
    
    if not client.initialize():
        print(f"❌ Failed to initialize server '{server_name}'")
        return
    
    print(f"\n🎯 Interactive Mode for '{server_name}'")
    print("Available commands:")
    print("  list - List all tools")
    print("  info <tool_name> - Show tool information")
    print("  call <tool_name> <json_params> - Call a tool")
    print("  search <query> - Search Wikipedia (if available)")
    print("  quit - Exit interactive mode")
    print("-" * 50)
    
    while True:
        try:
            command = input(f"\n[{server_name}]> ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not command:
                continue
            
            parts = command.split()
            if not parts:
                continue
            
            cmd = parts[0].lower()
            
            if cmd == 'list':
                client.display_tools(detailed=True)
            
            elif cmd == 'info' and len(parts) > 1:
                tool_name = parts[1]
                tool_info = client.get_tool_info(tool_name)
                if tool_info:
                    print(f"\n🔧 Tool: {tool_info.name}")
                    print(f"Description: {tool_info.description}")
                    if tool_info.input_schema:
                        import json
                        print(f"Schema: {json.dumps(tool_info.input_schema, indent=2)}")
                else:
                    print(f"❌ Tool '{tool_name}' not found")
            
            elif cmd == 'call' and len(parts) > 2:
                tool_name = parts[1]
                params_str = ' '.join(parts[2:])
                try:
                    import json
                    params = json.loads(params_str)
                    result = client.call_tool(tool_name, params)
                    display_results(result)
                except json.JSONDecodeError:
                    print("❌ Invalid JSON parameters")
                except Exception as e:
                    print(f"❌ Tool call failed: {e}")
            
            elif cmd == 'search' and len(parts) > 1:
                query = ' '.join(parts[1:])
                try:
                    result = client.search_wikipedia(query)
                    display_results(result)
                except Exception as e:
                    print(f"❌ Search failed: {e}")
            
            else:
                print("❌ Unknown command. Type 'list' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="MCP CLI Tool - Interact with Databricks MCP servers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
 Examples:
   %(prog)s list-servers
   %(prog)s list-tools wikipedia-search --detailed
   %(prog)s tool-info wikipedia-search rohit_dashora__docsearch__wikipedia_vi
   %(prog)s search "artificial intelligence"
   %(prog)s call-tool wikipedia-search rohit_dashora__docsearch__wikipedia_vi '{"query": "python"}'
   %(prog)s interactive wikipedia-search
   %(prog)s discover --backup
   %(prog)s discover --display-only
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List servers command
    subparsers.add_parser('list-servers', help='List all available MCP servers')
    
    # List tools command
    list_tools_parser = subparsers.add_parser('list-tools', help='List tools for a server')
    list_tools_parser.add_argument('server', help='Server name')
    list_tools_parser.add_argument('--detailed', action='store_true', help='Show detailed schema information')
    
    # Tool info command
    tool_info_parser = subparsers.add_parser('tool-info', help='Show detailed tool information')
    tool_info_parser.add_argument('server', help='Server name')
    tool_info_parser.add_argument('tool', help='Tool name')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search Wikipedia')
    search_parser.add_argument('query', help='Search query')
    
    # Call tool command
    call_tool_parser = subparsers.add_parser('call-tool', help='Call a specific tool')
    call_tool_parser.add_argument('server', help='Server name')
    call_tool_parser.add_argument('tool', help='Tool name')
    call_tool_parser.add_argument('parameters', help='JSON parameters')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive mode')
    interactive_parser.add_argument('server', help='Server name')
    
    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover tools and update configuration')
    discover_parser.add_argument('--display-only', action='store_true', help='Display tools without updating config')
    discover_parser.add_argument('--backup', action='store_true', help='Create backup before updating')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Create client manager
        manager = MCPClientManager()
        
        # Execute command
        if args.command == 'list-servers':
            list_servers(manager)
        
        elif args.command == 'list-tools':
            list_tools(manager, args.server, args.detailed)
        
        elif args.command == 'tool-info':
            show_tool_info(manager, args.server, args.tool)
        
        elif args.command == 'search':
            search_wikipedia(manager, args.query)
        
        elif args.command == 'call-tool':
            call_tool(manager, args.server, args.tool, args.parameters)
        
        elif args.command == 'interactive':
            interactive_mode(manager, args.server)
        
        elif args.command == 'discover':
            from mcp_discovery import discover_all_tools, display_discovered_tools, update_mcp_config
            
            # Create backup if requested
            if args.backup:
                import shutil
                backup_path = ".cursor/mcp.json.backup"
                shutil.copy2(".cursor/mcp.json", backup_path)
                print(f"📋 Created backup: {backup_path}")
            
            # Discover tools
            discovered_tools = discover_all_tools()
            
            if not discovered_tools:
                print("❌ No tools discovered")
                return
            
            # Display discovered tools
            display_discovered_tools(discovered_tools)
            
            # Update configuration if not display-only
            if not args.display_only:
                update_mcp_config(".cursor/mcp.json", discovered_tools)
                print(f"\n✅ Tool discovery complete! Updated .cursor/mcp.json")
            else:
                print(f"\n✅ Tool discovery complete! (Display only mode)")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 