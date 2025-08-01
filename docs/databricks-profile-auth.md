# Databricks Profile Authentication for MCP Client

This guide explains how to use existing Databricks CLI profiles for authentication with the MCP client, which is much simpler than setting up OAuth from scratch.

## 🔐 Why Use Databricks Profiles?

### **Benefits**
- ✅ **No additional setup** - Uses existing Databricks CLI configuration
- ✅ **Automatic token management** - Databricks CLI handles token refresh
- ✅ **Multiple workspaces** - Easy to switch between different Databricks workspaces
- ✅ **Standard approach** - Uses the same authentication as other Databricks tools
- ✅ **Secure storage** - Tokens stored in `~/.databrickscfg` file

### **How It Works**
1. **Databricks CLI** manages OAuth tokens automatically
2. **MCP client** reads tokens from your existing profiles
3. **No manual token management** required
4. **Seamless integration** with existing Databricks workflows

## 🛠️ Setup Instructions

### **Step 1: Install Databricks CLI**

```bash
# Install Databricks CLI
pip install databricks-cli

# Verify installation
databricks --version
```

### **Step 2: Configure Databricks Profiles**

#### **Option A: Interactive Configuration**
```bash
# Configure your first profile
databricks configure

# Configure additional profiles
databricks configure --profile wikipedia-search
databricks configure --profile doc-search
```

#### **Option B: Manual Configuration**
Create or edit `~/.databrickscfg`:

```ini
[wikipedia-search]
host = https://e2-demo-field-eng.cloud.databricks.com
token = your-oauth-token-here

[doc-search]
host = https://e2-demo-field-eng.cloud.databricks.com
token = your-oauth-token-here

[DEFAULT]
host = https://your-default-workspace.cloud.databricks.com
token = your-default-token-here
```

### **Step 3: Update MCP Configuration**

Replace your current `mcp.json` with profile-based configuration:

```json
{
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
```

### **Step 4: Test Profile Authentication**

```bash
# Test the profile authentication
python code/databricks_profile_auth.py

# Use MCP client with profile authentication
python code/mcp_cli.py list-servers
```

## 🔧 Profile Management

### **List Available Profiles**
```bash
# Using Databricks CLI
databricks configure --list

# Using our profile auth module
python -c "from databricks_profile_auth import DatabricksProfileAuth; auth = DatabricksProfileAuth(); print(auth.list_profiles())"
```

### **Switch Between Profiles**
```bash
# Set default profile
export DATABRICKS_CONFIG_PROFILE=wikipedia-search

# Or specify profile per command
DATABRICKS_CONFIG_PROFILE=wikipedia-search python code/mcp_cli.py list-servers
```

### **Validate Profile Configuration**
```bash
# Test if a profile is properly configured
python -c "
from databricks_profile_auth import DatabricksProfileAuth
auth = DatabricksProfileAuth()
print('Valid:', auth.validate_profile('wikipedia-search'))
print('Connection test:', auth.test_connection('wikipedia-search'))
"
```

## 🔄 Token Management

### **Automatic Token Refresh**
Databricks CLI automatically handles token refresh:
```bash
# Check token status
databricks tokens list

# Create new token
databricks tokens create --comment "MCP Client Token"

# Delete expired tokens
databricks tokens delete --token-id <token-id>
```

### **Token Expiration**
- **Personal Access Tokens**: Never expire (unless manually deleted)
- **OAuth Tokens**: Automatically refreshed by Databricks CLI
- **No manual intervention** required

## 🔍 Troubleshooting

### **Common Issues**

1. **"Profile not found" error**
   ```bash
   # Check available profiles
   databricks configure --list
   
   # Verify profile name in mcp.json matches ~/.databrickscfg
   ```

2. **"Invalid token" error**
   ```bash
   # Test profile authentication
   databricks clusters list --profile wikipedia-search
   
   # Create new token if needed
   databricks tokens create --profile wikipedia-search
   ```

3. **"Connection failed" error**
   ```bash
   # Test workspace connectivity
   databricks workspace ls --profile wikipedia-search
   
   # Check host URL format
   # Should be: https://workspace-name.cloud.databricks.com
   ```

### **Debug Mode**
```bash
# Enable debug logging
export DATABRICKS_VERBOSE=1

# Test with verbose output
databricks clusters list --profile wikipedia-search
```

## 📋 Migration from Bearer Tokens

### **Step-by-Step Migration**

1. **Backup current configuration**
   ```bash
   cp .cursor/mcp.json .cursor/mcp.json.backup
   ```

2. **Install Databricks CLI**
   ```bash
   pip install databricks-cli
   ```

3. **Configure profiles**
   ```bash
   databricks configure --profile wikipedia-search
   databricks configure --profile doc-search
   ```

4. **Update MCP configuration**
   ```bash
   cp .cursor/mcp-profile-example.json .cursor/mcp.json
   ```

5. **Test profile authentication**
   ```bash
   python code/databricks_profile_auth.py
   ```

6. **Remove old Bearer tokens** from configuration

### **Rollback Plan**
```bash
# Restore Bearer token configuration
cp .cursor/mcp.json.backup .cursor/mcp.json

# Continue using Bearer tokens
```

## 🔐 Security Best Practices

### **Profile Security**
1. **Secure file permissions**
   ```bash
   chmod 600 ~/.databrickscfg
   ```

2. **Use different profiles** for different environments
   ```ini
   [dev]
   host = https://dev-workspace.cloud.databricks.com
   token = dev-token
   
   [prod]
   host = https://prod-workspace.cloud.databricks.com
   token = prod-token
   ```

3. **Regular token rotation**
   ```bash
   # Create new token
   databricks tokens create --profile wikipedia-search
   
   # Update ~/.databrickscfg with new token
   # Delete old token
   databricks tokens delete --token-id <old-token-id>
   ```

### **Environment Variables**
```bash
# Set default profile
export DATABRICKS_CONFIG_PROFILE=wikipedia-search

# Add to shell profile
echo 'export DATABRICKS_CONFIG_PROFILE=wikipedia-search' >> ~/.bashrc
```

## 📚 Integration Examples

### **With MCP Client**
```python
from databricks_profile_auth import MCPDatabricksProfileAuth

# Initialize profile authentication
profile_auth = MCPDatabricksProfileAuth()

# Get token for specific server
token = profile_auth.get_token_for_server("wikipedia-search")

# Use with MCP client
# (The MCP client will automatically use profile authentication)
```

### **With Existing Databricks Tools**
```bash
# Use same profiles with other Databricks tools
databricks clusters list --profile wikipedia-search
databricks jobs list --profile doc-search
databricks workspace ls --profile DEFAULT
```

## 🎯 Benefits Over Manual OAuth

| Feature | Manual OAuth | Databricks Profiles |
|---------|-------------|-------------------|
| **Setup Complexity** | High | Low |
| **Token Management** | Manual | Automatic |
| **Multiple Workspaces** | Complex | Simple |
| **Integration** | Custom | Standard |
| **Maintenance** | High | Low |
| **Security** | Good | Excellent |

## 📚 Additional Resources

- [Databricks CLI Documentation](https://docs.databricks.com/dev-tools/cli/index.html)
- [Databricks Authentication](https://docs.databricks.com/dev-tools/auth.html)
- [MCP Client Documentation](README.md)

---

**Recommendation:** Use Databricks profiles for the simplest and most maintainable authentication solution! 🚀 