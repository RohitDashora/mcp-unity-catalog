# 🎯 Demo Project Notice

## ⚠️ **This is a Demo Project**

This repository contains a **demonstration implementation** of an MCP (Model Context Protocol) client for Databricks vector search. It is designed for **learning, testing, and prototyping purposes only**.

## 🎯 **Demo Purpose**

### **What This Project Demonstrates**
- **MCP Protocol Implementation** - Complete example of building MCP clients
- **Databricks Integration** - Vector search and authentication patterns  
- **CLI Development** - Interactive command-line interface design
- **Documentation Practices** - Visual documentation with diagrams
- **Code Organization** - Modular, maintainable code structure

### **Learning Objectives**
- 🧪 **Educational** - Learn MCP protocol and Databricks integration
- 🔬 **Testing** - Test vector search capabilities and authentication
- 🛠️ **Prototyping** - Build proof-of-concepts for MCP clients
- 📚 **Reference** - Code examples and patterns for MCP development

## 🚫 **Not Intended For**

- ❌ **Production Use** - This is a demo project
- ❌ **Commercial Deployment** - Use for learning and testing only
- ❌ **Enterprise Integration** - Reference implementation only
- ❌ **Direct Copy-Paste** - Use as reference, not production code

## 🚀 **Getting Started**

### **Quick Setup (5 minutes)**
```bash
# Clone the repository
git clone https://github.com/RohitDashora/mcp-unity-catalog.git
cd mcp-unity-catalog

# Setup environment
python3 -m venv mcp
source mcp/bin/activate
pip install -r code/requirements.txt

# Configure Databricks
databricks configure --profile your-profile

# Discover and configure
python scripts/find_vector_urls.py
cp .cursor/mcp-found-urls.json .cursor/mcp.json

# Test the demo
python code/mcp_cli.py list-servers
```

### **Documentation**
- **[📖 First-Time Setup](docs/first-time-setup.md)** - Complete setup guide
- **[📋 Quick Diagrams](docs/diagrams.md)** - Visual overview
- **[🏗️ Architecture](docs/architecture.md)** - System design
- **[🔄 Workflows](docs/workflows.md)** - Process flows

## 📊 **Demo Features**

### **Core Functionality**
- ✅ **Tool Discovery** - List and inspect MCP tools
- ✅ **Vector Search** - Query Databricks vector indexes
- ✅ **Authentication** - Profile-based and token-based auth
- ✅ **CLI Interface** - Interactive command-line tools
- ✅ **Multi-Server** - Work with multiple MCP servers

### **Documentation**
- ✅ **Visual Diagrams** - 17 Mermaid diagrams with PNG/SVG
- ✅ **Setup Guides** - Step-by-step instructions
- ✅ **Code Examples** - Working examples and patterns
- ✅ **Troubleshooting** - Common issues and solutions

## 🔧 **Demo Structure**

```
mcp-unity-catalog/
├── code/                    # Core Python modules
│   ├── mcp_client.py       # Main MCP client
│   ├── mcp_cli.py          # Command-line interface
│   ├── mcp_discovery.py    # Tool discovery
│   └── requirements.txt    # Dependencies
├── docs/                   # Comprehensive documentation
│   ├── diagrams/           # Mermaid source files
│   ├── images/             # Generated PNG/SVG diagrams
│   └── *.md               # Documentation guides
├── scripts/                # Automation scripts
└── .cursor/               # MCP configuration
```

## 🎓 **Learning Path**

1. **Start Here** - Read this DEMO.md file
2. **Setup** - Follow [First-Time Setup Guide](docs/first-time-setup.md)
3. **Explore** - Use the CLI to discover tools and features
4. **Study** - Review the code and documentation
5. **Experiment** - Modify and extend the demo
6. **Build** - Use patterns to create your own MCP clients

## 📝 **Contributing**

This is a demo project, but contributions are welcome:
- 🐛 **Bug Reports** - Help improve the demo
- 📚 **Documentation** - Enhance learning materials
- 🎨 **Examples** - Add more use cases
- 🔧 **Improvements** - Better code organization

## 📄 **License**

This demo project is provided as-is for educational purposes. Use at your own risk.

---

**🎯 Remember**: This is a **demo project** for learning and testing. Use it to understand MCP protocol implementation and Databricks integration patterns! 🚀 