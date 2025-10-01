# Mini Firewall - Packet Sorter

This Python script, `mini-firewall.py`, is a command-line tool that sorts packets from an input CSV file based on priority and serial number, and writes the sorted packets to an output CSV file. The script processes packets in chunks of 10, sorting each chunk independently and marking each batch in the output file.

## Features

- **CSV Input/Output**: Reads packet data from a CSV file and writes sorted data to another CSV file.
- **Flexible Delimiters**: Handles CSV files with different delimiters and ignores leading/trailing whitespace.
- **Error Handling**: Provides robust error handling for file operations, invalid data formats, and out-of-range priority values.
- **Chunk-based Sorting**: Sorts packets in chunks of 10 to avoid global sorting, processing each chunk independently.
- **Batch Marking**: Includes markers in the output file to delineate separate batches of sorted packets.
- **Command-Line Arguments**: Uses `argparse` for easy configuration of input and output file names.

## Usage

1.  **Prerequisites**:
    - Python 3.x

2.  **Running the Script**:

    ```bash
    python mini-firewall.py -i input.csv -o output.csv
    ```

    -   `-i` or `--input`: Specifies the input CSV file name (default: `input.csv`).
    -   `-o` or `--output`: Specifies the output CSV file name (default: `output.csv`).

3.  **Example `input.csv`**:

    ```csv
    SerialNo,Priority
    1,5
    2,3
    3,1
    4,3
    5,7
    6,10
    7,2
    8,4
    9,5
    10,1
    11,3
    12,5
    13,7
    14,2
    15,4
    16,6
    17,8
    18,9
    19,6
    20,8
    21,10
    22,1
    23,3
    24,5
    ```

4.  **Example `output.csv`**:

    ```csv
    SerialNo,Priority
    # Batch 1
    3,1
    10,1
    2,3
    4,3
    11,3
    1,5
    9,5
    12,5
    5,7
    6,10
    # Batch 2
    7,2
    14,2
    8,4
    15,4
    16,6
    19,6
    13,7
    17,8
    20,8
    18,9
    # Batch 3
    22,1
    23,3
    24,5
    21,10
    ```

## Implementation Details

-   **Loading Packets**: The `load_packets` function reads the input CSV file, handles comments, empty lines, and potential errors in data format.
-   **Sorting**: The `manual_sort` function sorts packets based on priority (ascending) and serial number (ascending).
-   **Chunk Processing**: The `main` function processes packets in chunks of 10, sorts each chunk, and writes the sorted chunks to the output file with batch markers.

## Error Handling

The script includes comprehensive error handling:

-   **FileNotFoundError**: Handles cases where the input file does not exist.
-   **ValueError**: Handles invalid data formats in the CSV file.
-   **Priority Range**: Checks if the priority value is within the valid range (1-10).
-   **General Exceptions**: Catches and reports any unexpected errors during file processing.