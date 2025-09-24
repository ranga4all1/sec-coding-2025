# Credential Manager

## Description

This program is a simple credential manager that allows users to store and retrieve API keys securely. It provides two storage options:

1.  **In-memory storage:** Stores the API keys in a hash table during the program's runtime. This is useful for temporary storage and quick access.
2.  **File storage:** Stores the API keys in a file, allowing persistent storage across program sessions.

The program encrypts the API keys before storing them, providing an additional layer of security.

## Logic

The program follows these steps:

1.  **Encryption Key Generation:**
    *   When the program starts, it generates an encryption key using the `Fernet` library. This key is used to encrypt and decrypt the API keys.
    *   **Note:** For demonstration purposes, the encryption key is stored in a file (`encryption.key`). **In a real-world application, this is highly insecure.** The key should be stored securely using a proper key management system.

2.  **Hashing:**
    *   Before encryption, the API key is hashed using SHA-256 to create a unique identifier.

3.  **Encryption:**
    *   The API key is encrypted using the `Fernet` cipher with the generated encryption key.

4.  **Storage:**
    *   **In-memory:** The service name and the encrypted API key are stored in a hash table.
    *   **File:** The service name, hashed key, and encrypted API key are stored in a file (`api_keys.txt`), each entry on a new line.

5.  **Retrieval:**
    *   The program retrieves the encrypted API key based on the service name.
    *   The encrypted API key is decrypted using the `Fernet` cipher.

## How to Use

1.  **Run the program:**

    ```bash
    python cred-manager.py
    ```

2.  **Choose an option:**

    The program presents a menu with the following options:

    *   **Store API key:** Allows you to store a new API key.
        *   Choose the storage option (in-memory or file).
        *   Enter the service name.
        *   Enter the API key.
    *   **Retrieve API key:** Allows you to retrieve an existing API key.
        *   Choose the retrieval option (from memory or from file).
        *   Enter the service name.
        *   The program will retrieve and display the decrypted API key.
    *   **List available keys:** Lists the service names for which keys are stored in memory and in the file.
    *   **Exit:** Exits the program.

## File Format

The `api_keys.txt` file stores the API keys in the following format: text
