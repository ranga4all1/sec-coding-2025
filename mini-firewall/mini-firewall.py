# Mini firewall - packet sorter
import argparse
import csv

def load_packets(filename):
    """Loads packets from a CSV file."""
    packets = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file, skipinitialspace=True)
            header_skipped = False
            for row_num, row in enumerate(reader):
                # Skip empty lines and comments
                if not row or not any(row) or row[0].startswith('#'):
                    continue

                row = [field.strip() for field in row]
                
                if len(row) != 2:
                    print(f"Warning: Line {row_num + 1} has invalid number of fields ({len(row)}), skipping.")
                    continue

                try:
                    SerialNo, priority = row
                    # Check if header needs to be skipped
                    if not header_skipped:
                        try:
                            int(SerialNo)
                            int(priority)
                            header_skipped = True
                        except ValueError:
                            print(f"Skipping header line: {row}")
                            continue  # Skip what is assumed to be the header
                    
                    SerialNo = int(SerialNo)
                    priority = int(priority)

                    if not 1 <= priority <= 10:
                        print(f"Warning: Priority {priority} is out of range (1-10) in line {row_num + 1}, skipping.")
                        continue

                    packets.append((SerialNo, priority))
                except ValueError:
                    print(f"Warning: Invalid data format in line {row_num + 1}: {row}, skipping.")
                except Exception as e:
                    print(f"Warning: Error processing line {row_num + 1}: {row} - {e}, skipping.")

        print(f"Loaded {len(packets)} packets from {filename}.")
    except FileNotFoundError:
        print(f"Error: {filename} file not found.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
    return packets


def manual_sort(packets):
    """Sorts packets based on priority and serial number."""
    return sorted(packets, key=lambda p: (p[1], p[0]))


def main(input_filename, output_filename):
    """Main function to process and sort packets in chunks."""
    print("Processing input file...")
    packets = load_packets(input_filename)
    print("--------------------------------\n")

    print("Sorting packets in chunks and writing to output file...")
    try:
        chunk_size = 10
        
        with open(output_filename, 'w') as file:
            file.write("SerialNo,Priority\n")  # Write header

            batch_number = 1
            for i in range(0, len(packets), chunk_size):
                chunk = packets[i:i + chunk_size]
                
                # Sort the chunk
                chunk_sorted = manual_sort(chunk)
                
                # Write the sorted chunk to the file
                file.write(f"# Batch {batch_number}\n")  # Batch marker
                for packet in chunk_sorted:
                    file.write(f"{packet[0]},{packet[1]}\n")
                
                batch_number += 1
                
        print(f"Packets sorted in chunks and written to {output_filename}.")

    except Exception as e:
        print(f"Error during sorting and writing: {e}")
        exit(1)
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