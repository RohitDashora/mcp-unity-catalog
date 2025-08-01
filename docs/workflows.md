# MCP Client Workflows

This document illustrates various workflows and usage patterns for the MCP client using Mermaid diagrams.

## 🚀 Quick Start Workflow

```mermaid
flowchart TD
    A[Clone Repository] --> B[Setup Virtual Environment]
    B --> C[Install Dependencies]
    C --> D[Load Environment Variables]
    D --> E[Discover Tools]
    E --> F[Start Using MCP Client]
    
    B --> B1[./scripts/setup_venv.sh]
    C --> C1[pip install -r requirements.txt]
    D --> D1[source scripts/load_env_simple.sh]
    E --> E1[python code/mcp_cli.py discover]
    F --> F1[python code/mcp_cli.py search 'query']
    
    style A fill:#e3f2fd
    style F fill:#e8f5e8
```

## 🔍 Tool Discovery Process

```mermaid
sequenceDiagram
    participant U as User
    participant CLI as CLI Tool
    participant MGR as Client Manager
    participant CLIENT as MCP Client
    participant SDK as Databricks SDK
    participant MCP as MCP Server
    participant CONFIG as mcp.json
    
    U->>CLI: discover --backup
    CLI->>MGR: Create manager
    MGR->>CONFIG: Load server config
    
    loop For each MCP server
        MGR->>CLIENT: Create client
        CLIENT->>SDK: Initialize connection
        SDK->>MCP: Connect to server
        MCP-->>SDK: Connection established
        CLIENT->>SDK: list_tools()
        SDK->>MCP: tools/list request
        MCP-->>SDK: Tool information
        SDK-->>CLIENT: Tool list
        CLIENT-->>MGR: Tool details
    end
    
    MGR->>CONFIG: Update with tool info
    CONFIG-->>MGR: Config updated
    MGR-->>CLI: Discovery complete
    CLI-->>U: Success message
```

## 🔐 Authentication Workflow

```mermaid
flowchart TD
    A[Start Authentication] --> B{Environment Variables Set?}
    
    B -->|Yes| C[Load Token from ENV<br/>MCP_*_TOKEN]
    B -->|No| D[Load Token from Config<br/>Authorization Header]
    
    C --> E[Extract Bearer Token]
    D --> E
    
    E --> F[Create WorkspaceClient]
    F --> G[Create DatabricksMCPClient]
    G --> H[Test Connection]
    
    H --> I{Connection Successful?}
    I -->|Yes| J[Authentication Complete]
    I -->|No| K[Authentication Failed]
    
    J --> L[Ready for Operations]
    K --> M[Error: Check Token/Network]
    
    style A fill:#e3f2fd
    style J fill:#e8f5e8
    style K fill:#ffebee
    style L fill:#e8f5e8
    style M fill:#ffebee
```

## 📋 Interactive Mode Workflow

```mermaid
flowchart TD
    A[Start Interactive Mode] --> B[Initialize Client]
    B --> C[Display Available Commands]
    C --> D[Wait for User Input]
    
    D --> E{Command Type}
    E -->|list| F[Display Tools]
    E -->|info| G[Show Tool Details]
    E -->|call| H[Execute Tool]
    E -->|search| I[Search Wikipedia]
    E -->|quit| J[Exit Mode]
    
    F --> K[Format and Display]
    G --> K
    H --> L[Execute with Parameters]
    I --> M[Search with Query]
    
    K --> D
    L --> N[Display Results]
    M --> N
    N --> D
    
    J --> O[Cleanup and Exit]
    
    style A fill:#e3f2fd
    style O fill:#e8f5e8
```

## 🔄 Configuration Management Workflow

```mermaid
flowchart LR
    subgraph "Configuration Sources"
        A[Environment Variables<br/>MCP_*_TOKEN]
        B[mcp.json<br/>Server Configuration]
        C[mcp.json<br/>Tool Information]
    end
    
    subgraph "Configuration Flow"
        D[Priority Check<br/>ENV > Config File]
        E[Token Extraction]
        F[Server Discovery]
        G[Tool Discovery]
    end
    
    subgraph "Configuration Updates"
        H[Backup Creation]
        I[Tool Info Update]
        J[Validation]
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

## 🛠️ Tool Execution Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant CLI as CLI Tool
    participant CLIENT as MCP Client
    participant SDK as Databricks SDK
    participant MCP as MCP Server
    
    U->>CLI: call-tool tool_name params
    CLI->>CLIENT: Initialize client
    CLIENT->>SDK: Create connection
    SDK->>MCP: Authenticate
    MCP-->>SDK: Authentication successful
    
    CLI->>CLIENT: call_tool(tool_name, params)
    CLIENT->>SDK: tools/call request
    SDK->>MCP: Execute tool
    MCP-->>SDK: Tool results
    SDK-->>CLIENT: Formatted results
    CLIENT-->>CLI: Results
    CLI-->>U: Display results
```

## 🔍 Search Workflow

```mermaid
flowchart TD
    A[User Search Query] --> B[Parse Query]
    B --> C[Find Wikipedia Tool]
    C --> D[Initialize Client]
    D --> E[Execute Search]
    E --> F[Process Results]
    F --> G[Format Output]
    G --> H[Display Results]
    
    E --> E1[Call rohit_dashora__docsearch__wikipedia_vi]
    F --> F1[Parse JSON Response]
    G --> G1[Extract Title, URL, Content]
    H --> H1[Show Formatted Results]
    
    style A fill:#e3f2fd
    style H fill:#e8f5e8
```

## 🚨 Error Handling Workflow

```mermaid
flowchart TD
    A[Operation Start] --> B{Configuration Valid?}
    B -->|No| C[Configuration Error]
    B -->|Yes| D{Environment Variables Set?}
    
    D -->|No| E[Use Config Token]
    D -->|Yes| F[Use ENV Token]
    
    E --> G[Initialize Client]
    F --> G
    
    G --> H{Connection Successful?}
    H -->|No| I[Connection Error]
    H -->|Yes| J[Execute Operation]
    
    J --> K{Operation Successful?}
    K -->|No| L[Operation Error]
    K -->|Yes| M[Return Results]
    
    C --> N[Display Error Message]
    I --> N
    L --> N
    
    N --> O[Suggest Solutions]
    O --> P[Log Error Details]
    
    style A fill:#e3f2fd
    style M fill:#e8f5e8
    style N fill:#ffebee
    style O fill:#fff3e0
```

## 🔄 Development Workflow

```mermaid
flowchart TD
    A[Add New MCP Server] --> B[Update mcp.json]
    B --> C[Set Environment Variables]
    C --> D[Test Connection]
    D --> E[Run Tool Discovery]
    E --> F[Verify Tools]
    F --> G[Test Tool Execution]
    G --> H[Document Usage]
    H --> I[Update Documentation]
    
    D --> D1{Connection OK?}
    D1 -->|No| D2[Debug Connection]
    D2 --> D
    
    F --> F1{Tools Found?}
    F1 -->|No| F2[Debug Discovery]
    F2 --> E
    
    G --> G1{Execution OK?}
    G1 -->|No| G2[Debug Execution]
    G2 --> G
    
    style A fill:#e3f2fd
    style I fill:#e8f5e8
```

## 📊 Data Flow Architecture

```mermaid
flowchart LR
    subgraph "Input Layer"
        A[User Commands]
        B[Configuration Files]
        C[Environment Variables]
    end
    
    subgraph "Processing Layer"
        D[Command Parser]
        E[Configuration Manager]
        F[Authentication Handler]
        G[Tool Executor]
    end
    
    subgraph "External Layer"
        H[Databricks SDK]
        I[MCP Servers]
        J[Result Formatter]
    end
    
    subgraph "Output Layer"
        K[Formatted Results]
        L[Error Messages]
        M[Logs]
    end
    
    A --> D
    B --> E
    C --> E
    
    D --> F
    E --> F
    F --> G
    
    G --> H
    H --> I
    I --> J
    
    J --> K
    G --> L
    F --> M
    
    style A fill:#e3f2fd
    style K fill:#e8f5e8
    style L fill:#ffebee
```

## 🎯 CLI Command Flow

```mermaid
flowchart TD
    A[mcp_cli.py] --> B{Command Type}
    
    B -->|list-servers| C[Load Config]
    B -->|list-tools| D[Initialize Client]
    B -->|tool-info| E[Get Tool Details]
    B -->|search| F[Execute Search]
    B -->|call-tool| G[Execute Tool]
    B -->|interactive| H[Start Interactive Mode]
    B -->|discover| I[Run Discovery]
    
    C --> J[Display Servers]
    D --> K[Show Tools]
    E --> L[Show Tool Info]
    F --> M[Search Results]
    G --> N[Tool Results]
    H --> O[Interactive Session]
    I --> P[Discovery Results]
    
    J --> Q[Format Output]
    K --> Q
    L --> Q
    M --> Q
    N --> Q
    O --> Q
    P --> Q
    
    Q --> R[Display to User]
    
    style A fill:#e3f2fd
    style R fill:#e8f5e8
```

## 🔧 Maintenance Workflow

```mermaid
flowchart TD
    A[Regular Maintenance] --> B[Check Token Validity]
    B --> C[Update Tool Discovery]
    C --> D[Test All Connections]
    D --> E[Update Documentation]
    E --> F[Backup Configuration]
    F --> G[Log Maintenance]
    
    B --> B1{Token Valid?}
    B1 -->|No| B2[Rotate Token]
    B2 --> B
    
    D --> D1{All OK?}
    D1 -->|No| D2[Debug Issues]
    D2 --> D
    
    style A fill:#e3f2fd
    style G fill:#e8f5e8
```

---

*These workflow diagrams provide detailed step-by-step processes for various operations in the MCP client system. They help users understand how different components interact and what to expect at each step.* 