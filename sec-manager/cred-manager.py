# Credential Manager

'''
Exercise: Secrets Manager

Design an API key storage system to store API keys for services. The
program should present two options to users to store and retrieve
passwords. You can use either an in-memory storage or store your
credentials in a file.

a) For storing, the program should ask for the inputs and store the password
securely. The inputs are:
String: ServiceName
String: APIKey

b) For retrieving the program asks for the service name and retrieves the
API key.
'''

import os
import hashlib
from cryptography.fernet import Fernet

# Constants
IN_MEMORY = 1
FILE_STORAGE = 2

# Generate a key for encryption
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

# Function to hash the API key
def hash_api_key(api_key):
    """Hashes the API key using SHA-256."""
    hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
    return hashed_key

# Function to encrypt the API key
def encrypt_api_key(api_key):
    """Encrypts the API key using Fernet."""
    encrypted_key = cipher.encrypt(api_key.encode())
    return encrypted_key

# Function to decrypt the API key
def decrypt_api_key(encrypted_key):
    """Decrypts the API key using Fernet."""
    decrypted_key = cipher.decrypt(encrypted_key).decode()
    return decrypted_key

# Function to store credentials in memory
def store_in_memory(hash_table, service_name, api_key):
    """Stores the service name and encrypted API key in memory."""
    hashed_key = hash_api_key(api_key)
    encrypted_key = encrypt_api_key(api_key)
    # Using service_name as key and encrypted API key as value
    insert(hash_table, service_name, (hashed_key, encrypted_key))
    print(f"API key for {service_name} stored in memory (encrypted).")

# Function to store credentials in a file
def store_in_file(filename, service_name, api_key):
    """Stores the service name and encrypted API key in a file."""
    hashed_key = hash_api_key(api_key)
    encrypted_key = encrypt_api_key(api_key)
    try:
        with open(filename, "a") as file:  # Open in append mode
            file.write(f"{service_name}:{hashed_key}:{encrypted_key.decode()}\n")
        print(f"API key for {service_name} stored in file (encrypted).")
    except Exception as e:
        print(f"Error storing in file: {e}")

# Function to retrieve credentials from memory
def retrieve_from_memory(hash_table, service_name):
    """Retrieves the encrypted API key from memory and returns it."""
    result = search(hash_table, service_name)
    if result:
        hashed_key, encrypted_key = result
        decrypted_key = decrypt_api_key(encrypted_key)
        print(f"API key (decrypted) for {service_name} retrieved from memory.")
        return decrypted_key
    else:
        print(f"No API key found for {service_name} in memory.")
        return None

# Function to retrieve credentials from a file
def retrieve_from_file(filename, service_name):
    """Retrieves the encrypted API key from a file and returns it."""
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 3:
                    s_name, hashed_key, encrypted_key_str = parts
                    if s_name == service_name:
                        encrypted_key = encrypted_key_str.encode()
                        decrypted_key = decrypt_api_key(encrypted_key)
                        print(f"API key (decrypted) for {service_name} retrieved from file.")
                        return decrypted_key
                else:
                    print(f"Invalid format in file: {line.strip()}")
        print(f"No API key found for {service_name} in file.")
        return None
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"Error retrieving from file: {e}")
        return None

# Function to list available service keys
def list_available_keys(hash_table, filename):
    """Lists the service names for which keys are stored."""
    print("\nAvailable Service Keys:")

    # List keys stored in memory
    print("\nIn Memory:")
    if hash_table:
        for bucket in hash_table:
            for pair in bucket:
                print(f"- {pair[0]}")
    else:
        print("No keys stored in memory.")

    # List keys stored in file
    print("\nIn File:")
    try:
        with open(filename, "r") as file:
            services = set()
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 3:
                    s_name, _, _ = parts
                    services.add(s_name)
            if services:
                for service in services:
                    print(f"- {service}")
            else:
                print("No keys stored in file.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error reading from file: {e}")

# Step 1: Define a hash function
# We'll use a simple hash function: value modulo table size
def simple_hash(key, table_size):
    return hash(key) % table_size


# Step 2: Create a hash table with chaining to handle collisions
def create_hash_table(size):
# Each slot will hold a list to handle collisions
    return [[] for _ in range(size)]


# Step 3: Insert a value into the hash table
def insert(hash_table, key, value):
    index = simple_hash(key, len(hash_table))
    print(f"Inserting ({key}, {value}) at index {index}")

    # Check if key already exists and update
    for pair in hash_table[index]:
        if pair[0] == key:
            pair[1] = value
            return
    # If not, append the key-value pair
    hash_table[index].append([key, value])


# Step 4: Search for a value by key
def search(hash_table, key):
    index = simple_hash(key, len(hash_table))
    print(f"Searching for key {key} at index {index}")
    for pair in hash_table[index]:
        if pair[0] == key:
            print(f"Found value: {pair[1]}")
            return pair[1]
    print("Key not found")
    return None

# Main function to interact with the user
def main():
    """Main function to interact with the user."""
    hash_table = create_hash_table(10)
    filename = "api_keys.txt"

    # Store the encryption key in a file (INSECURE - for demonstration purposes only)
    with open("encryption.key", "wb") as key_file:
        key_file.write(encryption_key)

    while True:
        print("\nChoose an option:")
        print("1. Store API key")
        print("2. Retrieve API key")
        print("3. List available keys")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            print("\nChoose storage option:")
            print("1. In-memory")
            print("2. In file")

            storage_choice = input("Enter your choice (1-2): ")

            service_name = input("Enter service name: ")
            api_key = input("Enter API key: ")

            if storage_choice == "1":
                store_in_memory(hash_table, service_name, api_key)
            elif storage_choice == "2":
                store_in_file(filename, service_name, api_key)
            else:
                print("Invalid storage choice.")

        elif choice == "2":
            print("\nChoose retrieval option:")
            print("1. From memory")
            print("2. From file")

            retrieval_choice = input("Enter your choice (1-2): ")

            service_name = input("Enter service name to retrieve: ")

            if retrieval_choice == "1":
                api_key = retrieve_from_memory(hash_table, service_name)
                if api_key:
                    print(f"Retrieved API key: {api_key}")
            elif retrieval_choice == "2":
                api_key = retrieve_from_file(filename, service_name)
                if api_key:
                    print(f"Retrieved API key: {api_key}")
            else:
                print("Invalid retrieval choice.")

        elif choice == "3":
            list_available_keys(hash_table, filename)

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()