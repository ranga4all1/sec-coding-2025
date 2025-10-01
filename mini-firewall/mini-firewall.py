# Mini firewall - packet sorter
import argparse

def load_packets(filename):
    """Loads packets from a CSV file."""
    packets = []
    try:
        with open(filename, 'r') as file:
            next(file)  # Skip header
            for line in file:
                SerialNo, priority = line.strip().split(',')
                packets.append((int(SerialNo), int(priority)))
        print(f"Loaded {len(packets)} packets from {filename}.")
    except FileNotFoundError:
        print(f"Error: {filename} file not found.")
        exit(1)
    except ValueError:
        print(f"Error: Invalid data format in {filename}.")
        exit(1)
    return packets


def manual_sort(packets):
    """Sorts packets based on priority and serial number."""
    n = len(packets)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if packets[j][1] < packets[min_idx][1] or \
               (packets[j][1] == packets[min_idx][1] and packets[j][0] < packets[min_idx][0]):
                min_idx = j
        packets[i], packets[min_idx] = packets[min_idx], packets[i]
    return packets


def write_packets(filename, packets):
    """Writes sorted packets to a CSV file."""
    try:
        with open(filename, 'w') as file:
            file.write("SerialNo,Priority\n")  # Write header
            for packet in packets:
                file.write(f"{packet[0]},{packet[1]}\n")
        print(f"Sorted packets written to {filename}.")
    except Exception as e:
        print(f"Error writing to {filename}: {e}")
        exit(1)


def main(input_filename, output_filename):
    """Main function to process and sort packets."""
    print("Processing input file...")
    packets = load_packets(input_filename)
    print("--------------------------------\n")

    print("Sorting packets by priority and serial number...")
    try:
        import time
        start_time = time.time()
        packets_sorted = manual_sort(packets)
        end_time = time.time()
        print(f"Sorting completed in {end_time - start_time:.6f} seconds.")
    except Exception as e:
        print(f"Error during sorting: {e}")
        exit(1)
    print(f"Sorted {len(packets_sorted)} packets.")
    print("--------------------------------\n")

    print("Writing sorted packets to output file...")
    write_packets(output_filename, packets_sorted)
    print("--------------------------------\n")

    print("Done.")
    print("--------------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini Firewall - Packet Sorter")
    parser.add_argument("-i", "--input", dest="input_file", default="input.csv",
                        help="Input CSV file name (default: input.csv)")
    parser.add_argument("-o", "--output", dest="output_file", default="output.csv",
                        help="Output CSV file name (default: output.csv)")
    args = parser.parse_args()

    main(args.input_file, args.output_file)