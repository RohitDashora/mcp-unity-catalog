# MCP Client Architecture

This document provides visual representations of the MCP client architecture using Mermaid diagrams.

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI[CLI Interface<br/>mcp_cli.py]
        LIB[Python Library<br/>mcp_client.py]
    end
    
    subgraph "Core Components"
        MGR[MCPClientManager<br/>Server Management]
        CLIENT[MCPClient<br/>Individual Server Client]
        DISCOVER[Tool Discovery<br/>mcp_discovery.py]
    end
    
    subgraph "Configuration Layer"
        CONFIG[mcp.json<br/>Server & Tool Config]
        ENV[Environment Variables<br/>MCP_*_TOKEN]
        BACKUP[Backup Files<br/>.backup]
    end
    
    subgraph "External Services"
        WIKI[Wikipedia Search<br/>MCP Server]
        DOCS[Documentation Search<br/>MCP Server]
        DATABRICKS[Databricks MCP SDK]
    end
    
    CLI --> MGR
    LIB --> MGR
    MGR --> CLIENT
    DISCOVER --> MGR
    
    CLIENT --> DATABRICKS
    DATABRICKS --> WIKI
    DATABRICKS --> DOCS
    
    MGR --> CONFIG
    CLIENT --> ENV
    DISCOVER --> BACKUP
    
    style CLI fill:#e1f5fe
    style LIB fill:#e1f5fe
    style MGR fill:#f3e5f5
    style CLIENT fill:#f3e5f5
    style DISCOVER fill:#f3e5f5
    style CONFIG fill:#e8f5e8
    style ENV fill:#e8f5e8
    style DATABRICKS fill:#fff3e0
```

## 🔄 Data Flow

```mermaid
flowchart TD
    A[User Input] --> B{Command Type}
    
    B -->|list-servers| C[Load Config]
    B -->|list-tools| D[Initialize Client]
    B -->|search| E[Execute Tool]
    B -->|discover| F[Tool Discovery]
    B -->|interactive| G[Interactive Mode]
    
    C --> H[Display Servers]
    D --> I[Connect to MCP Server]
    E --> I
    F --> J[Query All Servers]
    G --> K[Command Loop]
    
    I --> L{Use Environment Variables?}
    L -->|Yes| M[Load from ENV]
    L -->|No| N[Load from Config]
    
    M --> O[Create WorkspaceClient]
    N --> O
    O --> P[Create DatabricksMCPClient]
    P --> Q[Execute MCP Operations]
    
    J --> R[Discover Tools]
    R --> S[Update Config File]
    
    K --> T[Process Commands]
    T --> U[Display Results]
    
    Q --> U
    H --> U
    S --> U
    
    style A fill:#e3f2fd
    style U fill:#e8f5e8
    style M fill:#fff3e0
    style N fill:#fff3e0
```

## 🛠️ Tool Discovery Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant CLI as CLI Tool
    participant DIS as Discovery Script
    participant MGR as Client Manager
    participant CLIENT as MCP Client
    participant SDK as Databricks SDK
    participant MCP as MCP Server
    participant CONFIG as mcp.json
    
    U->>CLI: discover --backup
    CLI->>DIS: discover_all_tools()
    DIS->>MGR: Create ClientManager
    MGR->>CONFIG: Load server config
    
    loop For each server
        DIS->>MGR: get_client(server_name)
        MGR->>CLIENT: Create MCPClient
        CLIENT->>SDK: Initialize connection
        SDK->>MCP: Connect to server
        MCP-->>SDK: Connection established
        CLIENT->>SDK: list_tools()
        SDK->>MCP: tools/list request
        MCP-->>SDK: Tool information
        SDK-->>CLIENT: Tool list
        CLIENT-->>DIS: Tool details
    end
    
    DIS->>CONFIG: Update with tool info
    CONFIG-->>DIS: Config updated
    DIS-->>CLI: Discovery complete
    CLI-->>U: Success message
```

## 🔐 Authentication Flow

```mermaid
flowchart LR
    A[Start] --> B{Environment Variables Set?}
    
    B -->|Yes| C[Load from ENV<br/>MCP_*_TOKEN]
    B -->|No| D[Load from Config<br/>Authorization Header]
    
    C --> E[Extract Token]
    D --> E
    
    E --> F[Create WorkspaceClient]
    F --> G[Create DatabricksMCPClient]
    G --> H[Authenticate with Databricks]
    H --> I[Execute MCP Operations]
    
    style A fill:#e3f2fd
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style I fill:#e8f5e8
```

## 📋 CLI Command Structure

```mermaid
graph TD
    A[mcp_cli.py] --> B[list-servers]
    A --> C[list-tools]
    A --> D[tool-info]
    A --> E[search]
    A --> F[call-tool]
    A --> G[interactive]
    A --> H[discover]
    
    B --> I[Display available servers]
    C --> J[Show tools for server]
    D --> K[Show tool details]
    E --> L[Search Wikipedia]
    F --> M[Execute tool with params]
    G --> N[Interactive mode]
    H --> O[Discover and update config]
    
    J --> P[--detailed flag]
    O --> Q[--display-only flag]
    O --> R[--backup flag]
    
    style A fill:#e3f2fd
    style I fill:#e8f5e8
    style J fill:#e8f5e8
    style K fill:#e8f5e8
    style L fill:#e8f5e8
    style M fill:#e8f5e8
    style N fill:#e8f5e8
    style O fill:#e8f5e8
```

## 🔄 Configuration Management

```mermaid
graph LR
    subgraph "Configuration Sources"
        A[Environment Variables<br/>MCP_*_TOKEN]
        B[mcp.json<br/>Server Config]
        C[mcp.json<br/>Tools Config]
    end
    
    subgraph "Configuration Flow"
        D[Priority Check<br/>ENV > Config]
        E[Token Extraction]
        F[Server Discovery]
        G[Tool Discovery]
    end
    
    subgraph "Configuration Updates"
        H[Backup Creation]
        I[Tool Info Update]
        J[Config Validation]
    end
    
    A --> D
    B --> D
    C --> G
    
    D --> E
    E --> F
    F --> G
    
    G --> H
    H --> I
    I --> J
    
    style A fill:#e8f5e8
    style B fill:#fff3e0
    style C fill:#fff3e0
    style J fill:#e8f5e8
```

## 🎯 Usage Workflows

### Basic Usage Workflow

```mermaid
flowchart TD
    A[Setup Environment] --> B[Load Environment Variables]
    B --> C[List Available Servers]
    C --> D[Choose Server]
    D --> E[List Tools]
    E --> F[Execute Tool]
    F --> G[View Results]
    
    style A fill:#e3f2fd
    style G fill:#e8f5e8
```

### Advanced Usage Workflow

```mermaid
flowchart TD
    A[Setup Environment] --> B[Discover All Tools]
    B --> C[Update Configuration]
    C --> D[Interactive Mode]
    D --> E[Explore Tools]
    E --> F[Execute Custom Queries]
    F --> G[Save Results]
    
    style A fill:#e3f2fd
    style G fill:#e8f5e8
```

### Development Workflow

```mermaid
flowchart TD
    A[Add New MCP Server] --> B[Update mcp.json]
    B --> C[Set Environment Variables]
    C --> D[Run Tool Discovery]
    D --> E[Test Connection]
    E --> F[Execute Test Queries]
    F --> G[Document Usage]
    
    style A fill:#e3f2fd
    style G fill:#e8f5e8
```

## 🏛️ Class Relationships

```mermaid
classDiagram
    class MCPClientManager {
        -config_path: str
        -clients: Dict[str, MCPClient]
        +__init__(config_path)
        +get_client(server_name)
        +list_servers()
        +initialize_client(server_name)
        +display_servers()
        -_load_config()
    }
    
    class MCPClient {
        -workspace_hostname: str
        -token: str
        -server_url: str
        -mcp_client: DatabricksMCPClient
        -tools: List[ToolInfo]
        -_initialized: bool
        +__init__(workspace_hostname, token, server_url)
        +initialize()
        +list_tools()
        +get_tool_info(tool_name)
        +call_tool(tool_name, parameters)
        +display_tools(detailed)
        +search_wikipedia(query)
    }
    
    class ToolInfo {
        +name: str
        +description: str
        +input_schema: Optional[Dict]
        +__str__()
    }
    
    class MCPDiscovery {
        +discover_all_tools(config_path)
        +discover_tools_for_server(client, server_name)
        +update_mcp_config(config_path, discovered_tools)
        +display_discovered_tools(tools)
    }
    
    MCPClientManager --> MCPClient : manages
    MCPClient --> ToolInfo : contains
    MCPDiscovery --> MCPClientManager : uses
    MCPDiscovery --> ToolInfo : discovers
```

## 🔧 Component Dependencies

```mermaid
graph TD
    subgraph "Core Dependencies"
        A[databricks-mcp]
        B[databricks-sdk]
        C[requests]
    end
    
    subgraph "Our Components"
        D[mcp_client.py]
        E[mcp_cli.py]
        F[mcp_discovery.py]
    end
    
    subgraph "Configuration"
        G[mcp.json]
        H[Environment Variables]
    end
    
    subgraph "Scripts"
        I[setup_env.sh]
        J[load_env.sh]
        K[load_env_simple.sh]
    end
    
    D --> A
    D --> B
    E --> D
    F --> D
    D --> G
    D --> H
    I --> H
    J --> H
    K --> H
    
    style A fill:#fff3e0
    style B fill:#fff3e0
    style C fill:#fff3e0
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style F fill:#e3f2fd
```

## 📊 Error Handling Flow

```mermaid
flowchart TD
    A[Operation Start] --> B{Check Config}
    B -->|Missing| C[Config Error]
    B -->|Valid| D{Check Environment}
    
    D -->|No ENV| E[Use Config Token]
    D -->|Has ENV| F[Use ENV Token]
    
    E --> G[Initialize Client]
    F --> G
    
    G --> H{Connection Success?}
    H -->|No| I[Connection Error]
    H -->|Yes| J[Execute Operation]
    
    J --> K{Operation Success?}
    K -->|No| L[Operation Error]
    K -->|Yes| M[Return Results]
    
    C --> N[User-Friendly Error]
    I --> N
    L --> N
    
    style A fill:#e3f2fd
    style M fill:#e8f5e8
    style N fill:#ffebee
```

---

*These diagrams provide a comprehensive view of the MCP client architecture, data flow, and usage patterns. They help developers understand the system structure and can be used for documentation, presentations, and development planning.* 