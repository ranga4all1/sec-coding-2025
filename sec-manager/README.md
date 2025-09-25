# Credential Manager

## Description

This program is a credential manager that allows users to store and retrieve API keys securely. It provides three storage options:

1.  **SQLite Database:** Stores the API keys in an SQLite database, providing persistent storage across program sessions.
2.  **In-memory storage:** Stores the API keys in a hash table during the program's runtime. This is useful for temporary storage and quick access.
3.  **File storage:** Stores the API keys in a file, allowing persistent storage across program sessions.

The program encrypts the API keys before storing them, providing an additional layer of security.

## Dependencies

The program uses the following dependencies:

*   **sqlite3:** For interacting with the SQLite database.
*   **cryptography:** For encryption and decryption using Fernet.

To install the dependencies, use the following command:

```bash
pip install -r requirements.txt
```

## Logic

The program follows these steps:

1.  **Encryption Key Generation:**
    *   When the program starts, it attempts to load an encryption key from the `encryption.key` file. If the file does not exist, it generates a new key using the `Fernet` library and saves it to the file.
    *   **Warning:** For demonstration purposes, the encryption key is stored in a file (`encryption.key`). **In a real-world application, this is highly insecure.** The key should be stored securely using a proper key management system, such as a hardware security module (HSM) or a key vault.  Consider using environment variables or a more secure storage mechanism.  Treat this key with extreme care.

2.  **Hashing:**
    *   Before encryption, the API key is hashed using SHA-256 to create a unique identifier (used for file storage option).

3.  **Encryption:**
    *   The API key is encrypted using the `Fernet` cipher with the loaded or generated encryption key.

4.  **Storage:**
    *   **SQLite Database:** The service name and the encrypted API key are stored in the `api_keys` table in the `credentials.db` SQLite database.  The database is initialized if it doesn't exist.
    *   **In-memory:** The service name and the encrypted API key are stored in a hash table.
    *   **File:** The service name, hashed key, and encrypted API key are stored in a file (`api_keys.txt`), each entry on a new line.

5.  **Retrieval:**
    *   The program retrieves the encrypted API key based on the service name from the selected storage.
    *   The encrypted API key is decrypted using the `Fernet` cipher.

## Persistence

*   **SQLite Database:** API keys stored in the SQLite database (`credentials.db`) persist across program sessions.
*   **File:** API keys stored in the `api_keys.txt` file persist across program sessions.
*   **In-memory:** API keys stored in memory are lost when the program exits.

## How to Use

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the program:**

    ```bash
    python cred-manager.py
    ```

3.  **Choose an option:**

    The program presents a menu with the following options:

    *   **Store API key (SQLite):** Allows you to store a new API key in the SQLite database.
        *   Enter the service name.
        *   Enter the API key.
    *   **Retrieve API key (SQLite):** Allows you to retrieve an existing API key from the SQLite database.
        *   Enter the service name.
        *   The program will retrieve and display the decrypted API key.
    *   **Store API key (In-Memory/File):** Allows you to store a new API key in memory or in a file.
        *   Choose the storage option (in-memory or file).
        *   Enter the service name.
        *   Enter the API key.
    *   **Retrieve API key (In-Memory/File):** Allows you to retrieve an existing API key from memory or from a file.
        *   Choose the retrieval option (from memory or from file).
        *   Enter the service name.
        *   The program will retrieve and display the decrypted API key.
    *   **List available keys:** Lists the service names for which keys are stored in the SQLite database, memory, and file.
    *   **Exit:** Exits the program.

## File Formats

*   `api_keys.txt`: Stores the API keys in the following format: `service_name:hashed_key:encrypted_api_key`
*   `credentials.db`:  An SQLite database file containing a table named `api_keys` with columns `id`, `service`, and `api_key_encrypted`.
