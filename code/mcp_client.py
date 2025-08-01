"""
MCP (Model Context Protocol) Client for Databricks

This module provides a clean interface to interact with Databricks MCP servers,
allowing you to discover tools, view their schemas, and execute tool calls.
"""

from databricks_mcp import DatabricksMCPClient
from databricks.sdk import WorkspaceClient
import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Import profile authentication
try:
    from databricks_profile_auth import MCPDatabricksProfileAuth
    PROFILE_AUTH_AVAILABLE = True
except ImportError:
    PROFILE_AUTH_AVAILABLE = False


@dataclass
class ToolInfo:
    """Represents information about an MCP tool."""
    name: str
    description: str
    input_schema: Optional[Dict[str, Any]] = None
    
    def __str__(self) -> str:
        return f"Tool: {self.name}\nDescription: {self.description}\nSchema: {json.dumps(self.input_schema, indent=2) if self.input_schema else 'None'}"


class MCPClient:
    """
    A clean interface for interacting with Databricks MCP servers.
    
    This class provides methods to:
    - Connect to MCP servers
    - Discover available tools
    - View tool schemas and properties
    - Execute tool calls
    """
    
    def __init__(self, workspace_hostname: str, token: str, server_url: str):
        """
        Initialize the MCP client.
        
        Args:
            workspace_hostname: Databricks workspace hostname
            token: Authentication token
            server_url: MCP server URL
        """
        self.workspace_hostname = workspace_hostname
        self.token = token
        self.server_url = server_url
        self.mcp_client: Optional[DatabricksMCPClient] = None
        self.tools: List[ToolInfo] = []
        self._initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize the MCP client and discover available tools.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            print(f"🔗 Connecting to MCP server: {self.server_url}")
            
            # Create workspace client for authentication
            workspace_client = WorkspaceClient(
                host=self.workspace_hostname,
                token=self.token
            )
            
            # Create MCP client
            self.mcp_client = DatabricksMCPClient(
                server_url=self.server_url,
                workspace_client=workspace_client
            )
            
            # Discover tools
            print("🔍 Discovering available tools...")
            raw_tools = self.mcp_client.list_tools()
            
            # Convert to ToolInfo objects
            self.tools = []
            for tool in raw_tools:
                tool_info = ToolInfo(
                    name=tool.name,
                    description=tool.description,
                    input_schema=getattr(tool, 'input_schema', None)
                )
                self.tools.append(tool_info)
            
            self._initialized = True
            print(f"✅ Successfully discovered {len(self.tools)} tools")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize MCP client: {e}")
            return False
    
    def list_tools(self) -> List[ToolInfo]:
        """
        Get list of available tools.
        
        Returns:
            List of ToolInfo objects
        """
        if not self._initialized:
            raise RuntimeError("MCP client not initialized. Call initialize() first.")
        return self.tools
    
    def get_tool_info(self, tool_name: str) -> Optional[ToolInfo]:
        """
        Get information about a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            ToolInfo object if found, None otherwise
        """
        if not self._initialized:
            raise RuntimeError("MCP client not initialized. Call initialize() first.")
        
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """
        Call a specific tool with given parameters.
        
        Args:
            tool_name: Name of the tool to call
            parameters: Parameters to pass to the tool
            
        Returns:
            Tool execution result
        """
        if not self._initialized:
            raise RuntimeError("MCP client not initialized. Call initialize() first.")
        
        if not self.mcp_client:
            raise RuntimeError("MCP client not available")
        
        try:
            print(f"🚀 Calling tool '{tool_name}' with parameters: {parameters}")
            result = self.mcp_client.call_tool(tool_name, parameters)
            print("✅ Tool call successful")
            return result
        except Exception as e:
            print(f"❌ Tool call failed: {e}")
            raise
    
    def display_tools(self, detailed: bool = False):
        """
        Display available tools in a formatted way.
        
        Args:
            detailed: If True, show detailed schema information
        """
        if not self._initialized:
            print("❌ MCP client not initialized. Call initialize() first.")
            return
        
        print(f"\n📋 Available Tools ({len(self.tools)} found)")
        print("=" * 60)
        
        for i, tool in enumerate(self.tools, 1):
            print(f"\n{i}. {tool.name}")
            print(f"   Description: {tool.description}")
            
            if detailed and tool.input_schema:
                print(f"   Input Schema:")
                print(f"   {json.dumps(tool.input_schema, indent=6)}")
            
            print("-" * 40)
    
    def search_wikipedia(self, query: str) -> Any:
        """
        Convenience method to search Wikipedia using the vector search tool.
        
        Args:
            query: Search query
            
        Returns:
            Search results
        """
        # Find the Wikipedia search tool
        wikipedia_tool = None
        for tool in self.tools:
            if 'wikipedia' in tool.name.lower() or 'docsearch' in tool.name.lower():
                wikipedia_tool = tool
                break
        
        if not wikipedia_tool:
            raise ValueError("Wikipedia search tool not found")
        
        return self.call_tool(wikipedia_tool.name, {"query": query})


class MCPClientManager:
    """
    Manager class for handling multiple MCP clients and configurations.
    """
    
    def __init__(self, config_path: str = ".cursor/mcp.json"):
        """
        Initialize the MCP client manager.
        
        Args:
            config_path: Path to MCP configuration file
        """
        self.config_path = config_path
        self.clients: Dict[str, MCPClient] = {}
        self._load_config()
    
    def _load_config(self):
        """Load MCP configuration from file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"MCP config file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            mcp_servers = config.get('mcpServers', {})
            
            # Check if profile authentication is available and configured
            profile_auth = None
            if PROFILE_AUTH_AVAILABLE:
                profile_auth = MCPDatabricksProfileAuth(self.config_path)
                if profile_auth.list_configured_servers():
                    print("🔐 Using Databricks profile authentication")
            
            for server_name, server_config in mcp_servers.items():
                url = server_config['url']
                
                # Try profile authentication first
                token = None
                if profile_auth and server_name in profile_auth.list_configured_servers():
                    token = profile_auth.get_token_for_server(server_name)
                    if token:
                        print(f"🔐 Using profile authentication for: {server_name}")
                
                # Fall back to environment variable
                if not token:
                    env_token_name = f"MCP_{server_name.upper().replace('-', '_')}_TOKEN"
                    token = os.getenv(env_token_name)
                    if token:
                        print(f"🔐 Using token from environment variable: {env_token_name}")
                
                # Fall back to config file
                if not token:
                    auth_header = server_config['headers']['Authorization']
                    if auth_header.startswith('Bearer '):
                        token = auth_header.replace('Bearer ', '')
                        print(f"🔐 Using token from config file for: {server_name}")
                    elif auth_header == 'Bearer ${PROFILE_TOKEN}':
                        print(f"⚠️  Profile token placeholder found for {server_name}, but no profile configured")
                        continue
                
                if not token:
                    print(f"❌ No authentication token found for: {server_name}")
                    continue
                
                # Extract hostname from URL
                workspace_hostname = url.split('/')[2]  # e.g., "e2-demo-field-eng.cloud.databricks.com"
                
                client = MCPClient(workspace_hostname, token, url)
                self.clients[server_name] = client
                
        except Exception as e:
            raise Exception(f"Error loading MCP config: {e}")
    
    def get_client(self, server_name: str) -> Optional[MCPClient]:
        """
        Get an MCP client by server name.
        
        Args:
            server_name: Name of the server from config
            
        Returns:
            MCPClient instance if found, None otherwise
        """
        return self.clients.get(server_name)
    
    def list_servers(self) -> List[str]:
        """
        Get list of available server names.
        
        Returns:
            List of server names
        """
        return list(self.clients.keys())
    
    def initialize_client(self, server_name: str) -> bool:
        """
        Initialize a specific MCP client.
        
        Args:
            server_name: Name of the server to initialize
            
        Returns:
            True if successful, False otherwise
        """
        client = self.get_client(server_name)
        if not client:
            print(f"❌ Server '{server_name}' not found")
            return False
        
        return client.initialize()
    
    def display_servers(self):
        """Display available servers."""
        print(f"\n🌐 Available MCP Servers ({len(self.clients)} found)")
        print("=" * 50)
        
        for i, server_name in enumerate(self.clients.keys(), 1):
            print(f"{i}. {server_name}")
        print()


def display_results(result: Any, max_content_length: int = 200):
    """
    Display tool execution results in a formatted way.
    
    Args:
        result: Tool execution result
        max_content_length: Maximum length for content display
    """
    if not result:
        print("❌ No results returned")
        return
    
    print(f"\n📊 Results")
    print("=" * 50)
    
    try:
        # Handle different result types
        if hasattr(result, 'content'):
            content = result.content
        else:
            content = result
        
        # Try to parse as JSON
        if isinstance(content, str):
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                print(f"Raw content: {content[:max_content_length]}...")
                return
        else:
            data = content
        
        # Handle TextContent objects
        if hasattr(data, 'text'):
            try:
                data = json.loads(data.text)
            except (json.JSONDecodeError, AttributeError):
                data = str(data)
        
        # Handle different data structures
        if isinstance(data, list):
            print(f"Found {len(data)} results:")
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    print(f"\n{i}. {item.get('title', 'No title')}")
                    print(f"   URL: {item.get('url', 'No URL')}")
                    content_preview = item.get('content', 'No content')[:max_content_length]
                    print(f"   Content: {content_preview}...")
                else:
                    print(f"\n{i}. {str(item)[:max_content_length]}...")
                print("-" * 30)
        else:
            print(f"Result: {json.dumps(data, indent=2)}")
            
    except Exception as e:
        print(f"Error displaying results: {e}")
        print(f"Raw result: {result}")


def main():
    """
    Main function demonstrating MCP client usage.
    """
    print("🚀 MCP Client Demo")
    print("=" * 50)
    
    try:
        # Create client manager
        manager = MCPClientManager()
        manager.display_servers()
        
        # Get the Wikipedia search client
        client = manager.get_client("wikipedia-search")
        if not client:
            print("❌ Wikipedia search client not found")
            return
        
        # Initialize the client
        if not client.initialize():
            print("❌ Failed to initialize client")
            return
        
        # Display available tools
        client.display_tools(detailed=True)
        
        # Interactive mode
        print(f"\n🎯 Interactive Mode")
        print("Enter your search queries (type 'quit' to exit)")
        print("-" * 50)
        
        while True:
            query = input("\n🔍 Enter search query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                print("❌ Please enter a valid query")
                continue
            
            try:
                result = client.search_wikipedia(query)
                display_results(result)
            except Exception as e:
                print(f"❌ Search failed: {e}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 