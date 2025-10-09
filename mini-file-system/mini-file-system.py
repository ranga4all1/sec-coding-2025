# mini file system implementation in Python

"""
Here is what we will build:

Tree Structure: A file system is a tree where each node can be either a directory or a file
Root: The / directory is the root of our tree
Directories: Can contain other directories and files (parent-child relationships)
Files: Store text content and are leaf nodes (no children)
"""

class File:
    """Represents a file in the file system"""
    def __init__(self, name, content=""):
        self.name = name
        self.content = content
    
    def read(self):
        return self.content
    
    def write(self, content):
        self.content = content
    
    def __repr__(self):
        return f"File({self.name})"


class Directory:
    """Represents a directory in the file system"""
    def __init__(self, name):
        self.name = name
        self.children = {}  # Dictionary to store child directories and files
    
    def add_child(self, child):
        """Add a file or directory to this directory"""
        self.children[child.name] = child
    
    def remove_child(self, name):
        """Remove a child by name"""
        if name in self.children:
            del self.children[name]
            return True
        return False
    
    def get_child(self, name):
        """Get a child by name"""
        return self.children.get(name)
    
    def list_children(self):
        """List all children in this directory"""
        return list(self.children.keys())
    
    def __repr__(self):
        return f"Directory({self.name})"


class FileSystem:
    """Manages the entire file system"""
    def __init__(self):
        self.root = Directory("/")
    
    def _parse_path(self, path):
        """Parse a path like /home/documents/file.txt into parts"""
        # Remove leading/trailing slashes and split
        path = path.strip('/')
        if not path:
            return []
        return path.split('/')
    
    def _navigate_to_parent(self, path):
        """Navigate to the parent directory of the given path"""
        parts = self._parse_path(path)
        
        if not parts:
            return None, None
        
        # Navigate to parent directory
        current = self.root
        for part in parts[:-1]:  # All parts except the last one
            child = current.get_child(part)
            if child is None:
                return None, None
            if not isinstance(child, Directory):
                return None, None
            current = child
        
        return current, parts[-1]  # Return parent directory and target name
    
    def _navigate_to(self, path):
        """Navigate to a specific path and return the node"""
        parts = self._parse_path(path)
        
        if not parts:
            return self.root
        
        current = self.root
        for part in parts:
            child = current.get_child(part)
            if child is None:
                return None
            current = child
        
        return current
    
    def create_directory(self, path):
        """Create a new directory at the given path"""
        parent, name = self._navigate_to_parent(path)
        
        if parent is None:
            return False, "Invalid path: parent directory does not exist"
        
        if parent.get_child(name) is not None:
            return False, f"Directory or file '{name}' already exists"
        
        new_dir = Directory(name)
        parent.add_child(new_dir)
        return True, f"Directory '{path}' created successfully"
    
    def delete_directory(self, path):
        """Delete a directory at the given path"""
        parent, name = self._navigate_to_parent(path)
        
        if parent is None:
            return False, "Invalid path"
        
        child = parent.get_child(name)
        if child is None:
            return False, f"Directory '{name}' does not exist"
        
        if not isinstance(child, Directory):
            return False, f"'{name}' is not a directory"
        
        if child.children:
            return False, f"Directory '{name}' is not empty"
        
        parent.remove_child(name)
        return True, f"Directory '{path}' deleted successfully"
    
    def create_file(self, path, content=""):
        """Create a new file at the given path"""
        parent, name = self._navigate_to_parent(path)
        
        if parent is None:
            return False, "Invalid path: parent directory does not exist"
        
        if parent.get_child(name) is not None:
            return False, f"File or directory '{name}' already exists"
        
        new_file = File(name, content)
        parent.add_child(new_file)
        return True, f"File '{path}' created successfully"
    
    def read_file(self, path):
        """Read the content of a file"""
        node = self._navigate_to(path)
        
        if node is None:
            return False, "File does not exist"
        
        if not isinstance(node, File):
            return False, "Path is not a file"
        
        return True, node.read()
    
    def delete_file(self, path):
        """Delete a file at the given path"""
        parent, name = self._navigate_to_parent(path)
        
        if parent is None:
            return False, "Invalid path"
        
        child = parent.get_child(name)
        if child is None:
            return False, f"File '{name}' does not exist"
        
        if not isinstance(child, File):
            return False, f"'{name}' is not a file"
        
        parent.remove_child(name)
        return True, f"File '{path}' deleted successfully"
    
    def list_directory(self, path="/"):
        """List contents of a directory"""
        node = self._navigate_to(path)
        
        if node is None:
            return False, "Directory does not exist"
        
        if not isinstance(node, Directory):
            return False, "Path is not a directory"
        
        contents = []
        for name, child in node.children.items():
            if isinstance(child, Directory):
                contents.append(f"[DIR]  {name}")
            else:
                contents.append(f"[FILE] {name}")
        
        return True, contents
    
    def display_tree(self, path="/"):
        """Display the file system as a visual tree structure"""
        node = self._navigate_to(path)
        
        if node is None:
            return False, "Path does not exist"
        
        if not isinstance(node, Directory):
            return False, "Path is not a directory"
        
        result = [f"{path if path != '/' else '/'}"]
        self._display_tree_recursive(node, "", True, result)
        return True, "\n".join(result)
    
    def _display_tree_recursive(self, directory, prefix, is_last, result):
        """Recursively build the tree structure"""
        children = list(directory.children.items())
        
        for i, (name, child) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            
            # Choose the right symbols
            connector = "└── " if is_last_child else "├── "
            
            # Add type indicator
            if isinstance(child, Directory):
                result.append(f"{prefix}{connector}📁 {name}/")
                
                # Recursively display children of this directory
                extension = "    " if is_last_child else "│   "
                self._display_tree_recursive(child, prefix + extension, is_last_child, result)
            else:
                result.append(f"{prefix}{connector}📄 {name}")



def print_menu():
    """Display the menu options"""
    print("\n" + "="*50)
    print("MINI FILE SYSTEM")
    print("="*50)
    print("1. Create a new directory")
    print("2. Delete a directory")
    print("3. Create a file")
    print("4. Read a file")
    print("5. Delete a file")
    print("6. List directory contents")
    print("7. Display tree structure")
    print("8. Exit")
    print("="*50)


def main():
    """Main function to run the interactive file system"""
    fs = FileSystem()
    
    print("Welcome to the Mini File System!")
    print("Root directory '/' has been created.")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            # Create directory
            path = input("Enter directory path (e.g., /home/documents): ").strip()
            success, message = fs.create_directory(path)
            print(f"\n{'✓' if success else '✗'} {message}")
        
        elif choice == '2':
            # Delete directory
            path = input("Enter directory path to delete: ").strip()
            success, message = fs.delete_directory(path)
            print(f"\n{'✓' if success else '✗'} {message}")
        
        elif choice == '3':
            # Create file
            path = input("Enter file path (e.g., /home/readme.txt): ").strip()
            content = input("Enter file content: ").strip()
            success, message = fs.create_file(path, content)
            print(f"\n{'✓' if success else '✗'} {message}")
        
        elif choice == '4':
            # Read file
            path = input("Enter file path to read: ").strip()
            success, result = fs.read_file(path)
            if success:
                print(f"\n✓ File content:")
                print(f"--- {path} ---")
                print(result)
                print("-" * (len(path) + 8))
            else:
                print(f"\n✗ {result}")
        
        elif choice == '5':
            # Delete file
            path = input("Enter file path to delete: ").strip()
            success, message = fs.delete_file(path)
            print(f"\n{'✓' if success else '✗'} {message}")
        
        elif choice == '6':
            # List directory
            path = input("Enter directory path to list (press Enter for root): ").strip()
            if not path:
                path = "/"
            success, result = fs.list_directory(path)
            if success:
                print(f"\n✓ Contents of '{path}':")
                if result:
                    for item in result:
                        print(f"  {item}")
                else:
                    print("  (empty)")
            else:
                print(f"\n✗ {result}")
        
        elif choice == '7':
            # Display tree structure
            path = input("Enter directory path to display (press Enter for root): ").strip()
            if not path:
                path = "/"
            success, result = fs.display_tree(path)
            if success:
                print(f"\n✓ Tree structure:")
                print(result)
            else:
                print(f"\n✗ {result}")
        
        elif choice == '8':
            # Exit
            print("\nThank you for using Mini File System. Goodbye!")
            break
        
        else:
            print("\n✗ Invalid choice. Please enter a number between 1 and 8.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()