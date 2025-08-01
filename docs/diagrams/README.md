# MCP Client Diagrams

This directory contains Mermaid diagram files (`.mmd`) for the MCP client system. These files can be converted to PNG, SVG, or other image formats for use in documentation, presentations, or web pages.

## 📁 File Structure

```
docs/diagrams/
├── README.md                    # This file
├── *.mmd                        # Mermaid diagram files
├── png/                         # PNG output directory (generated)
└── svg/                         # SVG output directory (generated)
```

## 🎨 Available Diagrams

### System Overview
- `system-overview.mmd` - High-level system architecture
- `detailed-architecture.mmd` - Detailed component relationships
- `component-dependencies.mmd` - Dependency relationships

### Workflows
- `basic-workflow.mmd` - Basic usage workflow
- `quick-start-workflow.mmd` - Quick start process
- `interactive-mode-workflow.mmd` - Interactive mode flow
- `tool-discovery-workflow.mmd` - Tool discovery sequence

### Authentication & Commands
- `authentication-flow.mmd` - Authentication process
- `cli-commands.mmd` - CLI command structure
- `tool-discovery.mmd` - Tool discovery process

### Technical Details
- `data-flow.mmd` - Data flow through the system
- `class-relationships.mmd` - Class relationships
- `error-handling-flow.mmd` - Error handling process

### Usage Examples
- `usage-examples.mmd` - Usage examples and commands

## 🔧 Converting Diagrams

### Using the Conversion Script

```bash
# Make the script executable (if not already)
chmod +x scripts/convert_diagrams.sh

# Run the conversion script
./scripts/convert_diagrams.sh
```

### Manual Conversion with mmdc

```bash
# Convert to PNG
mmdc -i docs/diagrams/system-overview.mmd -o docs/diagrams/png/system-overview.png

# Convert to SVG
mmdc -i docs/diagrams/system-overview.mmd -o docs/diagrams/svg/system-overview.svg
```

### Using Docker

```bash
# Convert to PNG
docker run --rm -v $PWD:/data minlag/mermaid-cli -i docs/diagrams/system-overview.mmd -o docs/diagrams/png/system-overview.png

# Convert to SVG
docker run --rm -v $PWD:/data minlag/mermaid-cli -i docs/diagrams/system-overview.mmd -o docs/diagrams/svg/system-overview.svg
```

## 📦 Installing mmdc

### Option 1: npm
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Option 2: yarn
```bash
yarn global add @mermaid-js/mermaid-cli
```

### Option 3: Docker
```bash
# Pull the Docker image
docker pull minlag/mermaid-cli
```

## 🎯 Usage Examples

### In Documentation
```markdown
![System Overview](docs/diagrams/png/system-overview.png)
```

### In Presentations
- Use PNG files for PowerPoint/Keynote
- Use SVG files for web presentations

### In Web Pages
```html
<img src="docs/diagrams/svg/system-overview.svg" alt="System Overview">
```

## 🔄 Updating Diagrams

1. Edit the `.mmd` file
2. Run the conversion script
3. The updated images will be generated automatically

## 🎨 Customization

You can customize the diagrams by:
- Modifying colors in the `style` statements
- Changing the diagram type (graph, flowchart, sequenceDiagram, etc.)
- Adding or removing components
- Adjusting the layout and flow

## 📋 Diagram Types

- **graph**: General purpose diagrams
- **flowchart**: Process flow diagrams
- **sequenceDiagram**: Interaction sequences
- **classDiagram**: Class relationships
- **gantt**: Timeline diagrams
- **pie**: Pie charts

## 🚀 Tips

- Use transparent backgrounds for better integration
- Keep diagrams focused on one concept
- Use consistent naming conventions
- Add comments to complex diagrams
- Test diagrams in the target format

---

*For more information about Mermaid syntax, visit [mermaid.js.org](https://mermaid.js.org/)* 