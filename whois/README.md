# Whois Lookup Utility

## Summary

This Python script performs WHOIS lookups on a list of domains to retrieve the registrar information. It supports multiple input methods (command-line arguments, CSV file), output formats (text, CSV, JSON), and parallel processing for faster lookups.

## Code Logic

1.  **Argument Parsing:** Uses `argparse` to handle command-line arguments for domains, input file, output format, and output file path.
2.  **Domain Input:** Reads domains either directly from the command line or from a CSV file.
3.  **Parallel Lookups:** Uses `threading` and `queue` to perform WHOIS lookups in parallel, improving performance for large lists of domains.
4.  **WHOIS Lookup:** Employs the `python-whois` library to query WHOIS servers and extract registrar information. It handles potential errors and retries failed lookups.
5.  **Output Formatting:** Formats the results into text, CSV, or JSON format using `pandas`.
6.  **Output:** Prints the results to standard output or saves them to a file.

## Usage Examples

### 1. Provide domains as command-line arguments:

```bash
python whois-utility.py example.com openai.com
```
This command will perform WHOIS lookups for example.com and openai.com and print the results to the console in CSV format.

### 2. Provide a file path:
```bash
python whois-utility.py --file domains.csv
```
This command will read domains from the domains.csv file (one domain per line) and perform WHOIS lookups.

### 3. Specify the output file:
```bash
python whois-utility.py example.com --output results.csv

```
This command will save the WHOIS lookup results for example.com to the results.csv file.

### 4. Specify the output format:
```bash
python whois-utility.py --format json example.com
```
This command will perform a WHOIS lookup for example.com and print the results to the console in JSON format. Other supported formats are csv and text.

Example domains.csv file:
```
example.com
openai.com
google.com
```