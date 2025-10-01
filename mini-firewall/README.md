# Mini Firewall - Packet Sorter

## Description

This Python script simulates a mini firewall by sorting packets based on their priority and serial number. It reads packet data from a CSV file, sorts the packets, and writes the sorted data to another CSV file.

## Code Logic

1.  **Packet Loading:**
    *   The script reads packet data from a CSV file specified by the user.
    *   The `load_packets` function opens the CSV file, skips the header, and reads each line, extracting the serial number and priority of each packet.
    *   The packet data is stored as a list of tuples, where each tuple contains the serial number and priority of a packet.
    *   Error handling is included to catch `FileNotFoundError` and `ValueError` exceptions.

2.  **Packet Sorting:**
    *   The script sorts the packets based on priority and serial number using a manual sorting algorithm.
    *   The `manual_sort` function implements a selection sort algorithm to sort the packets.
    *   Packets are primarily sorted by priority (lower priority values are placed earlier in the sorted list).
    *   If two packets have the same priority, they are sorted by serial number (lower serial numbers are placed earlier).

3.  **Packet Writing:**
    *   The script writes the sorted packet data to a CSV file specified by the user.
    *   The `write_packets` function opens the output CSV file and writes a header row ("SerialNo,Priority").
    *   It then iterates through the sorted list of packets and writes each packet's serial number and priority to a new line in the CSV file.
    *   Error handling is included to catch potential exceptions during file writing.

## Usage

1.  **Run the script:**

    ```bash
    python mini-firewall.py -i input.csv -o output.csv
    ```

2.  **Arguments:**

    *   `-i` or `--input`: Specifies the input CSV file name. Default is `input.csv`.
    *   `-o` or `--output`: Specifies the output CSV file name. Default is `output.csv`.

3.  **CSV File Format:**

    The input CSV file should have the following format:

    ```csv
    SerialNo,Priority
    1,5
    2,3
    3,1
    ...
    ```

    *   `SerialNo`: The serial number of the packet (integer).
    *   `Priority`: The priority of the packet (integer). Lower values indicate higher priority.

4.  **Example:**

    If you have an input CSV file named `input.csv` with the following content:

    ```csv
    SerialNo,Priority
    1,5
    2,3
    3,1
    4,3
    5,7
    6,10
    ```

    Running the script with the command:

    ```bash
    python mini-firewall.py -i input.csv -o output.csv
    ```

    will produce an output CSV file named `output.csv` with the following content:

    ```csv
    SerialNo,Priority
    3,1
    2,3
    4,3
    1,5
    5,7
    6,10
    ```