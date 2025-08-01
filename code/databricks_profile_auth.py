#!/usr/bin/env python3
"""
Databricks Profile Authentication for MCP Client

This module integrates with the existing Databricks CLI profile system
to use OAuth tokens from your configured Databricks profiles.
"""

import os
import json
import subprocess
import requests
from typing import Dict, Optional, Any
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DatabricksProfile:
    """Represents a Databricks CLI profile configuration."""
    name: str
    host: str
    token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class DatabricksProfileAuth:
    """Authentication using Databricks CLI profiles."""
    
    def __init__(self, profile_name: Optional[str] = None):
        self.profile_name = profile_name or os.getenv('DATABRICKS_CONFIG_PROFILE', 'DEFAULT')
        self.profiles_dir = Path.home() / '.databrickscfg'
        self.profiles: Dict[str, DatabricksProfile] = {}
        self._load_profiles()
    
    def _load_profiles(self):
        """Load all Databricks profiles from ~/.databrickscfg."""
        if not self.profiles_dir.exists():
            print(f"⚠️  Databricks config file not found: {self.profiles_dir}")
            return
        
        try:
            # Parse the .databrickscfg file
            current_profile = None
            with open(self.profiles_dir, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_profile = line[1:-1]
                        self.profiles[current_profile] = DatabricksProfile(name=current_profile, host='')
                    elif '=' in line and current_profile:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key == 'host':
                            self.profiles[current_profile].host = value
                        elif key == 'token':
                            self.profiles[current_profile].token = value
                        elif key == 'username':
                            self.profiles[current_profile].username = value
                        elif key == 'password':
                            self.profiles[current_profile].password = value
                        elif key == 'auth_type':
                            # Handle auth_type = databricks-cli (newer authentication)
                            if value == 'databricks-cli':
                                print(f"🔐 Profile '{current_profile}' uses databricks-cli authentication")
            
            print(f"📋 Loaded {len(self.profiles)} Databricks profiles")
            
        except Exception as e:
            print(f"❌ Error loading Databricks profiles: {e}")
    
    def get_profile(self, profile_name: Optional[str] = None) -> Optional[DatabricksProfile]:
        """Get a specific profile by name."""
        name = profile_name or self.profile_name
        return self.profiles.get(name)
    
    def list_profiles(self) -> list:
        """List all available profile names."""
        return list(self.profiles.keys())
    
    def get_token_from_profile(self, profile_name: Optional[str] = None) -> Optional[str]:
        """Get OAuth token from a specific profile."""
        profile = self.get_profile(profile_name)
        if not profile:
            print(f"❌ Profile '{profile_name or self.profile_name}' not found")
            return None
        
        if profile.token:
            return profile.token
        
        # For profiles with auth_type = databricks-cli, always use CLI
        return self._get_token_via_cli(profile_name or self.profile_name)
    
    def _get_token_via_cli(self, profile_name: str) -> Optional[str]:
        """Get token using databricks CLI command."""
        try:
            # Use the newer databricks auth token command
            result = subprocess.run(
                ['databricks', 'auth', 'token', '--profile', profile_name, '--output', 'JSON'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                token_data = json.loads(result.stdout)
                return token_data.get('access_token')
            
            print(f"⚠️  No token found for profile '{profile_name}': {result.stderr}")
            return None
            
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout getting token for profile '{profile_name}'")
            return None
        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting token for profile '{profile_name}': {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error getting token: {e}")
            return None
    
    def get_workspace_hostname(self, profile_name: Optional[str] = None) -> Optional[str]:
        """Get workspace hostname from profile."""
        profile = self.get_profile(profile_name)
        if profile and profile.host:
            # Extract hostname from URL
            if profile.host.startswith('https://'):
                return profile.host[8:]  # Remove 'https://'
            elif profile.host.startswith('http://'):
                return profile.host[7:]   # Remove 'http://'
            return profile.host
        return None
    
    def validate_profile(self, profile_name: Optional[str] = None) -> bool:
        """Validate that a profile has the necessary configuration."""
        profile = self.get_profile(profile_name)
        if not profile:
            return False
        
        # Check if we have either a token or username/password
        has_token = bool(profile.token)
        has_credentials = bool(profile.username and profile.password)
        
        # For databricks-cli auth, we don't need explicit credentials in the file
        if not has_token and not has_credentials:
            # Try to get token via CLI to validate
            test_token = self._get_token_via_cli(profile_name or self.profile_name)
            if test_token:
                return True
            else:
                print(f"❌ Profile '{profile.name}' missing authentication credentials")
                return False
        
        if not profile.host:
            print(f"❌ Profile '{profile.name}' missing host configuration")
            return False
        
        return True
    
    def test_connection(self, profile_name: Optional[str] = None) -> bool:
        """Test connection to Databricks workspace using profile."""
        profile = self.get_profile(profile_name)
        if not profile:
            return False
        
        token = self.get_token_from_profile(profile_name)
        if not token:
            return False
        
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(f'https://{profile.host}/api/2.0/clusters/list', headers=headers)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False


class MCPDatabricksProfileAuth:
    """MCP-specific integration with Databricks profiles."""
    
    def __init__(self, config_path: str = ".cursor/mcp.json"):
        self.config_path = config_path
        self.profile_auth = DatabricksProfileAuth()
        self.server_profiles: Dict[str, str] = {}
        self._load_server_profiles()
    
    def _load_server_profiles(self):
        """Load profile mappings from MCP configuration."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            for server_name, server_config in config.get('mcpServers', {}).items():
                # Check if server has a profile mapping
                profile_name = server_config.get('profile')
                if profile_name:
                    self.server_profiles[server_name] = profile_name
                    print(f"🔗 Mapped server '{server_name}' to profile '{profile_name}'")
                
        except FileNotFoundError:
            print(f"⚠️  MCP config file not found: {self.config_path}")
        except Exception as e:
            print(f"❌ Error loading server profiles: {e}")
    
    def get_token_for_server(self, server_name: str) -> Optional[str]:
        """Get OAuth token for a specific MCP server."""
        profile_name = self.server_profiles.get(server_name)
        if not profile_name:
            print(f"⚠️  No profile mapping found for server '{server_name}'")
            return None
        
        return self.profile_auth.get_token_from_profile(profile_name)
    
    def get_hostname_for_server(self, server_name: str) -> Optional[str]:
        """Get workspace hostname for a specific MCP server."""
        profile_name = self.server_profiles.get(server_name)
        if not profile_name:
            return None
        
        return self.profile_auth.get_workspace_hostname(profile_name)
    
    def list_configured_servers(self) -> list:
        """List MCP servers with profile mappings."""
        return list(self.server_profiles.keys())
    
    def validate_server_config(self, server_name: str) -> bool:
        """Validate configuration for a specific server."""
        profile_name = self.server_profiles.get(server_name)
        if not profile_name:
            return False
        
        return self.profile_auth.validate_profile(profile_name)


# Example usage and configuration
def example_profile_config():
    """Example MCP configuration using Databricks profiles."""
    return {
        "mcpServers": {
            "wikipedia-search": {
                "type": "streamable-http",
                "url": "https://e2-demo-field-eng.cloud.databricks.com/api/2.0/mcp/vector-search/rohit_dashora/docsearch",
                "headers": {
                    "Authorization": "Bearer ${PROFILE_TOKEN}"
                },
                "profile": "wikipedia-search",
                "note": "Databricks MCP server using profile authentication"
            },
            "doc-search": {
                "type": "streamable-http",
                "url": "https://e2-demo-field-eng.cloud.databricks.com/api/2.0/mcp/vector-search/mervekarali_catalog/multi_agent",
                "headers": {
                    "Authorization": "Bearer ${PROFILE_TOKEN}"
                },
                "profile": "doc-search",
                "note": "Databricks MCP server using profile authentication"
            }
        }
    }


def example_databricks_config():
    """Example ~/.databrickscfg file content."""
    return """
[wikipedia-search]
host = https://e2-demo-field-eng.cloud.databricks.com
token = your-oauth-token-here

[doc-search]
host = https://e2-demo-field-eng.cloud.databricks.com
token = your-oauth-token-here

[DEFAULT]
host = https://your-default-workspace.cloud.databricks.com
token = your-default-token-here
"""


if __name__ == "__main__":
    # Example usage
    print("🔐 Databricks Profile Authentication for MCP")
    print("=============================================")
    
    # Initialize profile authentication
    profile_auth = DatabricksProfileAuth()
    
    # List available profiles
    profiles = profile_auth.list_profiles()
    print(f"📋 Available profiles: {profiles}")
    
    if profiles:
        # Test the first profile
        test_profile = profiles[0]
        print(f"\n🧪 Testing profile: {test_profile}")
        
        if profile_auth.validate_profile(test_profile):
            token = profile_auth.get_token_from_profile(test_profile)
            if token:
                print(f"✅ Token obtained: {token[:20]}...")
                
                if profile_auth.test_connection(test_profile):
                    print("✅ Connection test successful!")
                else:
                    print("❌ Connection test failed")
            else:
                print("❌ Failed to get token")
        else:
            print("❌ Profile validation failed")
    else:
        print("\n💡 No Databricks profiles found!")
        print("To set up profiles:")
        print("1. Install Databricks CLI: pip install databricks-cli")
        print("2. Configure profiles: databricks configure")
        print("3. Or manually create ~/.databrickscfg file") 