# First-Time Setup Guide

## 🚀 **Complete Setup Guide for New Users**

This guide will walk you through setting up the MCP client from scratch, including how to find your Databricks URLs and configure everything properly.

![Setup Options](../images/setup-options.png)

*Choose your preferred setup experience: Quick Start (5 minutes), Detailed Guide, or Advanced Configuration*

## 📋 **Prerequisites**

Before starting, ensure you have:
- ✅ **Python 3.8+** installed
- ✅ **Git** installed
- ✅ **Access to a Databricks workspace** with vector search capabilities
- ✅ **Databricks CLI** (we'll install this during setup)

## 🎯 **Step 1: Clone and Setup the Repository**

```bash
# Clone the repository
git clone <your-repository-url>
cd mcp-unity-catalog

# Create and activate virtual environment
python3 -m venv mcp
source mcp/bin/activate  # On Windows: mcp\Scripts\activate

# Install dependencies
pip install -r code/requirements.txt

# Optional: Install development dependencies (for contributors)
# pip install -r code/requirements-dev.txt
```

## 🔐 **Step 2: Setup Databricks Authentication**

### **Option A: Databricks Profile Authentication (Recommended)**

```bash
# Install Databricks CLI
pip install databricks-cli

# Configure your profile
databricks configure --profile your-profile-name

# You'll be prompted for:
# - Databricks Host: https://your-workspace.cloud.databricks.com
# - Username: your-email@company.com
# - Password: your-password
```

### **Option B: Personal Access Token**

If you prefer using a personal access token:

1. **Generate a token in Databricks:**
   - Go to your Databricks workspace
   - Click on your profile picture → **User Settings**
   - Go to **Access Tokens** tab
   - Click **Generate New Token**
   - Copy the token (you won't see it again!)

2. **Configure with token:**
   ```bash
   databricks configure --profile your-profile-name --token
   # Enter your workspace URL and the token you just generated
   ```

## 🔍 **Step 3: Find Your Vector Search URLs**

### **Method 1: From Databricks UI**

1. **Navigate to Vector Search:**
   - Go to your Databricks workspace
   - Click **Machine Learning** in the left sidebar
   - Click **Vector Search**

2. **Find your indexes:**
   - Look for existing vector search indexes
   - Note down the **Catalog**, **Schema**, and **Index Name**

3. **Construct the URL:**
   ```
   https://your-workspace.cloud.databricks.com/api/2.0/mcp/vector-search/CATALOG/SCHEMA
   ```

### **Method 2: Using Databricks CLI**

```bash
# List all catalogs
databricks unity-catalog catalogs list

# List schemas in a catalog
databricks unity-catalog schemas list --catalog-name YOUR_CATALOG

# List vector search indexes
databricks ml vector-search indexes list --catalog-name YOUR_CATALOG --schema-name YOUR_SCHEMA
```

### **Method 3: Using the URL Finder Script (Recommended)**

![URL Discovery Workflow](../images/url-discovery-workflow.png)

*Automated URL discovery process that finds your vector search indexes*

We've created a helper script that automatically discovers your vector search URLs:

```bash
# Run the URL finder script
python scripts/find_vector_urls.py

# This will:
# 1. Find all your catalogs and schemas
# 2. Discover vector search indexes
# 3. Generate a complete mcp.json configuration
# 4. Save it as .cursor/mcp-found-urls.json
```

### **Method 3: From Existing Code/Configuration**

If you already have vector search working in your environment:

```bash
# Look for existing configurations
find . -name "*.json" -exec grep -l "vector-search" {} \;

# Or check your Databricks notebooks for vector search calls
```

## ⚙️ **Step 4: Configure mcp.json**

### **Create Your Configuration**

1. **Copy the working example:**
   ```bash
   cp .cursor/mcp-profile-working.json .cursor/mcp.json
   ```

2. **Edit the configuration:**
   ```bash
   # Open the file in your preferred editor
   nano .cursor/mcp.json
   # or
   code .cursor/mcp.json
   ```

3. **Update with your details:**
   ```json
   {
     "mcpServers": {
       "wikipedia-search": {
         "type": "streamable-http",
         "url": "https://YOUR_WORKSPACE.cloud.databricks.com/api/2.0/mcp/vector-search/YOUR_CATALOG/YOUR_SCHEMA",
         "headers": {
           "Authorization": "Bearer ${PROFILE_TOKEN}"
         },
         "profile": "YOUR_PROFILE_NAME",
         "note": "Databricks MCP server using profile authentication"
       }
     }
   }
   ```

### **Configuration Examples**

#### **Single Server Setup**
```json
{
  "mcpServers": {
    "my-search": {
      "type": "streamable-http",
      "url": "https://my-workspace.cloud.databricks.com/api/2.0/mcp/vector-search/my_catalog/my_schema",
      "headers": {
        "Authorization": "Bearer ${PROFILE_TOKEN}"
      },
      "profile": "my-profile",
      "note": "My vector search server"
    }
  }
}
```

#### **Multiple Servers Setup**
```json
{
  "mcpServers": {
    "wikipedia-search": {
      "type": "streamable-http",
      "url": "https://workspace1.cloud.databricks.com/api/2.0/mcp/vector-search/catalog1/schema1",
      "headers": {
        "Authorization": "Bearer ${PROFILE_TOKEN}"
      },
      "profile": "profile1",
      "note": "Wikipedia search server"
    },
    "documentation-search": {
      "type": "streamable-http",
      "url": "https://workspace2.cloud.databricks.com/api/2.0/mcp/vector-search/catalog2/schema2",
      "headers": {
        "Authorization": "Bearer ${PROFILE_TOKEN}"
      },
      "profile": "profile2",
      "note": "Documentation search server"
    }
  }
}
```

## 🧪 **Step 5: Test Your Setup**

![Quick Start Workflow](../images/quick-start-workflow.png)

*Complete setup workflow showing all steps from clone to ready-to-use*

### **Verify Configuration**
```bash
# List available servers
python code/mcp_cli.py list-servers

# Expected output:
# 🌐 Available MCP Servers (1 found)
# ==================================================
# 1. wikipedia-search
```

### **Discover Available Tools**
```bash
# Discover tools on your server
python code/mcp_cli.py discover

# This will update your mcp.json with discovered tools
```

### **Test a Search**
```bash
# Test with a simple search
python code/mcp_cli.py search "test query"

# Or use interactive mode
python code/mcp_cli.py interactive
```

## 🔧 **Step 6: Troubleshooting**

![Troubleshooting Flow](../images/troubleshooting-flow.png)

*Visual guide for resolving common setup issues*

### **Common Issues and Solutions**

#### **Issue: "No authentication token found"**
```bash
# Solution: Verify your profile is configured
databricks auth token --profile your-profile-name

# If this fails, reconfigure your profile
databricks configure --profile your-profile-name
```

#### **Issue: "Connection refused" or "404 Not Found"**
- ✅ **Check your workspace URL** - Make sure it's correct
- ✅ **Verify the vector search endpoint** - Ensure the catalog/schema exists
- ✅ **Check permissions** - Ensure you have access to the vector search index

#### **Issue: "Profile not found"**
```bash
# List all configured profiles
databricks auth list

# Reconfigure if needed
databricks configure --profile your-profile-name
```

#### **Issue: "JSON parsing error"**
- ✅ **This is a known SDK issue** - It doesn't affect functionality
- ✅ **Tool calls still work** - You can ignore this error
- ✅ **Check the actual results** - They should be returned correctly

### **Debug Commands**

```bash
# Test profile authentication
python -c "
from code.databricks_profile_auth import DatabricksProfileAuth
auth = DatabricksProfileAuth('.cursor/mcp.json')
print('Profiles:', auth.list_configured_servers())
print('Token test:', auth.get_token_for_server('your-server-name')[:20] + '...')
"

# Test MCP client directly
python -c "
from code.mcp_client import MCPClientManager
manager = MCPClientManager('.cursor/mcp.json')
print('Servers:', list(manager.clients.keys()))
"
```

## 📚 **Step 7: Next Steps**

### **Explore Available Commands**
```bash
# Get help
python code/mcp_cli.py --help

# List all available commands
python code/mcp_cli.py list-servers
python code/mcp_cli.py list-tools wikipedia-search
python code/mcp_cli.py tool-info wikipedia-search tool-name
python code/mcp_cli.py call-tool wikipedia-search tool-name '{"param": "value"}'
```

### **Generate Documentation**
```bash
# Generate visual diagrams
./scripts/generate_diagrams.sh

# View the diagrams
open docs/images/README.md
```

### **Set Up Environment Variables (Optional)**
```bash
# Load environment variables for easier access
source scripts/load_env_simple.sh

# Or add to your shell profile
echo 'source /path/to/mcp-unity-catalog/scripts/load_env_simple.sh' >> ~/.bashrc
```

## 🎯 **Quick Reference**

### **Essential Commands**
```bash
# Setup
python3 -m venv mcp && source mcp/bin/activate
pip install -r code/requirements.txt
databricks configure --profile your-profile

# Configuration
cp .cursor/mcp-profile-working.json .cursor/mcp.json
# Edit .cursor/mcp.json with your URLs

# Testing
python code/mcp_cli.py list-servers
python code/mcp_cli.py discover
python code/mcp_cli.py search "test query"
```

### **URL Format**
```
https://WORKSPACE.cloud.databricks.com/api/2.0/mcp/vector-search/CATALOG/SCHEMA
```

### **Configuration Structure**
```json
{
  "mcpServers": {
    "server-name": {
      "type": "streamable-http",
      "url": "YOUR_VECTOR_SEARCH_URL",
      "headers": {"Authorization": "Bearer ${PROFILE_TOKEN}"},
      "profile": "YOUR_PROFILE_NAME"
    }
  }
}
```

## 🆘 **Getting Help**

- 📖 **Read the main README**: `README.md`
- 🔍 **Check troubleshooting**: `docs/profile-auth-test-results.md`
- 🎨 **View diagrams**: `docs/images/README.md`
- 📋 **See project summary**: `SUMMARY.md`

---

**🎉 Congratulations!** You've successfully set up the MCP client. You can now interact with your Databricks vector search indexes programmatically! 🚀 