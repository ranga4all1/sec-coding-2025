# Credential Manager

'''
Exercise: Secrets Manager

Design an API key storage system to store API keys for services. The
program should present two options to users to store and retrieve
passwords. You can use either an in-memory storage or store your
credentials in a file.

For storing, the program should ask for the inputs and store the password
securely. The inputs are:
String: ServiceName
String: APIKey

For retrieving the program asks for the service name and retrieves the
API key.
'''


# Step 1: Define a hash function
# We'll use a simple hash function: value modulo table size
def simple_hash(key, table_size):
    return key % table_size
# 5 %10 = 5
# 10% 10 = 0
# 11%10 = 1


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


# Step 5: Demonstrate the hash table
hash_table = create_hash_table(10)

# Define some API keys as constants
OPENAI_API_KEY = 1001
GROK_API_KEY = 1002
GOOGLE_API_KEY = 1003
AWS_API_KEY = 1004
ORACLE_API_KEY = 1005
AZURE_API_KEY = 1006
IBM_API_KEY = 1007
SALESFORCE_API_KEY = 1008
SLACK_API_KEY = 1009

# Insert some key-value pairs
insert(hash_table, OPENAI_API_KEY, "A1B1C1")
insert(hash_table, GROK_API_KEY, "A2B2C2")
insert(hash_table, GOOGLE_API_KEY, "A3B3C3")
insert(hash_table, AWS_API_KEY, "A4B4C4")
insert(hash_table, ORACLE_API_KEY, "A5B5C5")
insert(hash_table, AZURE_API_KEY, "A6B6C6")
insert(hash_table, IBM_API_KEY, "A7B7C7")
insert(hash_table, SALESFORCE_API_KEY, "A8B8C8")
insert(hash_table, SLACK_API_KEY, "A9B9C9")

print("\nHash Table State:")
for i, bucket in enumerate(hash_table):
    print(f"Index {i}: {bucket}")
print("\nSearch Examples:")

print("Searching for OpenAI API Key:")
search(hash_table, OPENAI_API_KEY)
print("Searching for AWS API Key:")
search(hash_table, AWS_API_KEY)
print("Searching for Slack API Key:")
search(hash_table, SLACK_API_KEY)
