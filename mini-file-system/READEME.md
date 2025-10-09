# Mini File System

A Python-based mini file system implementation that demonstrates tree and graph data structures through an interactive command-line interface.

## Overview

This project simulates a hierarchical file system where users can create, read, and delete directories and files. The file system is represented as a tree structure with the root directory (`/`) at the top and directories/files as child nodes.

## Data Structures & Logic

### Core Components

1. **File Class**: Represents a file node with name and text content
2. **Directory Class**: Represents a directory node with children stored in a dictionary (hash map)
3. **FileSystem Class**: Manages the entire tree structure and provides operations

### Key Algorithms

- **Tree Traversal**: Uses depth-first search (DFS) to navigate through the file system hierarchy
- **Path Parsing**: Converts string paths (e.g., `/home/documents/file.txt`) into navigable components
- **Recursive Tree Display**: Implements DFS to visualize the tree structure with ASCII art

### Tree Structure

```
Root (/)
├── Directory (children: dict)
│   ├── File (content: string)
│   └── Directory
│       └── File
└── Directory
```

## Features

1. **Create Directory** - Add new directories at any path
2. **Delete Directory** - Remove empty directories
3. **Create File** - Create files with text content
4. **Read File** - Display file contents
5. **Delete File** - Remove files from the system
6. **List Directory** - Show contents of a directory
7. **Display Tree** - Visualize the entire file system structure with emojis and ASCII art

## Usage

### Running the Program

```bash
python mini-file-system.py
```

### Example Workflow

```
1. Create directory: /home
2. Create directory: /home/documents
3. Create file: /home/documents/readme.txt with content "Hello World"
4. Display tree structure to see the hierarchy
5. Read file: /home/documents/readme.txt
6. Delete file: /home/documents/readme.txt
7. Delete directory: /home/documents
```

### Sample Tree Output

```
/
├── 📁 home/
│   ├── 📁 documents/
│   │   ├── 📄 readme.txt
│   │   └── 📄 notes.txt
│   └── 📁 pictures/
│       └── 📄 photo.jpg
```

## Path Format

- All paths must start with `/` (root)
- Directories end with `/` in the tree display
- Example: `/home/documents/file.txt`

## Error Handling

- Cannot delete non-empty directories
- Cannot create duplicate files/directories
- Invalid paths are caught and reported
- Type checking (file vs directory) is enforced

## Requirements

- Python 3.6 or higher
- No external dependencies required