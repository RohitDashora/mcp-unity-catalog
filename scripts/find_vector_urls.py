#!/usr/bin/env python3
"""
Vector Search URL Finder

This script helps users find their Databricks vector search URLs
by using the Databricks CLI to list catalogs, schemas, and indexes.
"""

import json
import subprocess
import sys
from typing import List, Dict, Optional

def run_databricks_command(cmd: List[str]) -> Optional[Dict]:
    """Run a databricks CLI command and return JSON output."""
    try:
        result = subprocess.run(
            ['databricks'] + cmd + ['--output', 'JSON'],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"❌ Command failed: {' '.join(cmd)}")
            print(f"Error: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print(f"⏰ Command timed out: {' '.join(cmd)}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON response from: {' '.join(cmd)}")
        return None
    except FileNotFoundError:
        print("❌ Databricks CLI not found. Please install it first:")
        print("   pip install databricks-cli")
        return None

def get_workspace_url() -> Optional[str]:
    """Get the current workspace URL from Databricks CLI."""
    try:
        result = subprocess.run(
            ['databricks', 'workspace', 'list', '--output', 'JSON'],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode == 0:
            # Try to extract workspace URL from the command
            config_result = subprocess.run(
                ['databricks', 'config', 'get', '--output', 'JSON'],
                capture_output=True, text=True, timeout=10
            )
            
            if config_result.returncode == 0:
                config = json.loads(config_result.stdout)
                return config.get('host')
        
        return None
    except:
        return None

def list_catalogs() -> List[Dict]:
    """List all catalogs."""
    print("🔍 Finding catalogs...")
    result = run_databricks_command(['unity-catalog', 'catalogs', 'list'])
    
    if result and 'catalogs' in result:
        return result['catalogs']
    return []

def list_schemas(catalog_name: str) -> List[Dict]:
    """List schemas in a catalog."""
    print(f"🔍 Finding schemas in catalog '{catalog_name}'...")
    result = run_databricks_command([
        'unity-catalog', 'schemas', 'list',
        '--catalog-name', catalog_name
    ])
    
    if result and 'schemas' in result:
        return result['schemas']
    return []

def list_vector_indexes(catalog_name: str, schema_name: str) -> List[Dict]:
    """List vector search indexes in a schema."""
    print(f"🔍 Finding vector indexes in '{catalog_name}.{schema_name}'...")
    result = run_databricks_command([
        'ml', 'vector-search', 'indexes', 'list',
        '--catalog-name', catalog_name,
        '--schema-name', schema_name
    ])
    
    if result and 'indexes' in result:
        return result['indexes']
    return []

def generate_mcp_config(workspace_url: str, indexes: List[Dict]) -> Dict:
    """Generate MCP configuration from found indexes."""
    config = {"mcpServers": {}}
    
    for idx, index in enumerate(indexes):
        catalog = index.get('catalog_name', 'unknown_catalog')
        schema = index.get('schema_name', 'unknown_schema')
        index_name = index.get('name', f'index_{idx}')
        
        server_name = f"{catalog}_{schema}".replace('-', '_').lower()
        
        config["mcpServers"][server_name] = {
            "type": "streamable-http",
            "url": f"{workspace_url}/api/2.0/mcp/vector-search/{catalog}/{schema}",
            "headers": {
                "Authorization": "Bearer ${PROFILE_TOKEN}"
            },
            "profile": "your-profile-name",
            "note": f"Vector search server for {catalog}.{schema}"
        }
    
    return config

def main():
    """Main function to find vector search URLs."""
    print("🚀 Vector Search URL Finder")
    print("=" * 50)
    
    # Get workspace URL
    workspace_url = get_workspace_url()
    if not workspace_url:
        print("❌ Could not determine workspace URL.")
        print("Please ensure you have configured Databricks CLI:")
        print("   databricks configure --profile your-profile")
        sys.exit(1)
    
    print(f"🏢 Workspace: {workspace_url}")
    print()
    
    # Find catalogs
    catalogs = list_catalogs()
    if not catalogs:
        print("❌ No catalogs found or no access to Unity Catalog.")
        print("Please ensure you have Unity Catalog access.")
        sys.exit(1)
    
    print(f"📚 Found {len(catalogs)} catalogs:")
    for catalog in catalogs:
        print(f"   - {catalog.get('name', 'unknown')}")
    print()
    
    # Find schemas and indexes
    all_indexes = []
    
    for catalog in catalogs:
        catalog_name = catalog.get('name')
        if not catalog_name:
            continue
            
        schemas = list_schemas(catalog_name)
        
        for schema in schemas:
            schema_name = schema.get('name')
            if not schema_name:
                continue
                
            indexes = list_vector_indexes(catalog_name, schema_name)
            
            if indexes:
                print(f"✅ Found {len(indexes)} vector indexes in {catalog_name}.{schema_name}:")
                for index in indexes:
                    index_name = index.get('name', 'unknown')
                    print(f"   - {index_name}")
                    all_indexes.append(index)
                print()
    
    if not all_indexes:
        print("❌ No vector search indexes found.")
        print("Please ensure you have vector search indexes created in your workspace.")
        sys.exit(1)
    
    # Generate MCP configuration
    print("🔧 Generating MCP configuration...")
    config = generate_mcp_config(workspace_url, all_indexes)
    
    # Save configuration
    config_file = ".cursor/mcp-found-urls.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to: {config_file}")
    print()
    
    # Display URLs
    print("🌐 Vector Search URLs Found:")
    print("=" * 50)
    
    for server_name, server_config in config["mcpServers"].items():
        url = server_config["url"]
        note = server_config["note"]
        print(f"📡 {server_name}:")
        print(f"   URL: {url}")
        print(f"   Note: {note}")
        print()
    
    print("📋 Next Steps:")
    print("1. Review the generated configuration:")
    print(f"   cat {config_file}")
    print()
    print("2. Copy it to your main config:")
    print("   cp .cursor/mcp-found-urls.json .cursor/mcp.json")
    print()
    print("3. Edit the profile names in .cursor/mcp.json")
    print()
    print("4. Test your configuration:")
    print("   python code/mcp_cli.py list-servers")

if __name__ == "__main__":
    main() 