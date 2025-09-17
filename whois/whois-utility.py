# Whois Lookup Script 

# python script that calls a whois server to lookup the registrar of a list of domains

# install the required package
# ! pip install python-whois


import whois
import pandas as pd
import threading
import time
import queue
import random
import argparse
import json

def lookup_registrar(domain_queue, results):
    while True:
        try:
            domain = domain_queue.get(timeout=3)  # Timeout to exit thread gracefully
            retries = 3
            for attempt in range(retries):
                try:
                    w = whois.whois(domain)
                    registrar = getattr(w, 'registrar', 'Not found')
                    results.append({'domain': domain, 'registrar': registrar})
                    break  # Success, break retry loop
                except Exception as e:
                    if attempt < retries - 1:
                        wait_time = (2 ** attempt) + random.random()  # Exponential backoff + jitter
                        print(f"Retrying {domain} in {wait_time:.2f} seconds after error: {e}")
                        time.sleep(wait_time)
                    else:
                        results.append({'domain': domain, 'registrar': f'Error: {e}'})
                        print("**FINAL OUTPUT**") # Print before final error result
                finally:
                    pass # No action needed here
            domain_queue.task_done()
        except queue.Empty:
            break

def main():
    parser = argparse.ArgumentParser(description='Whois Lookup Script')
    parser.add_argument('domains', nargs='*', help='List of domains to lookup')
    parser.add_argument('--file', help='Path to a CSV file containing a list of domains')
    parser.add_argument('--format', choices=['text', 'csv', 'json'], default='csv', help='Output format (text, csv, json)')
    parser.add_argument('--output', help='Output file path. If not specified, prints to stdout.')

    args = parser.parse_args()

    domains = []

    # 1. Get domains from command line or file
    if args.domains:
        domains = args.domains
    elif args.file:
        try:
            domains_df = pd.read_csv(args.file, header=None, names=['domain'], dtype={'domain': str})
            domains_df = domains_df.dropna()  # Remove rows with NaN values
            domains = domains_df['domain'].tolist()
            domains = [d.strip() for d in domains] # Remove whitespace
        except FileNotFoundError:
            print(f"Error: {args.file} not found.")
            print("**FINAL OUTPUT**")
            return
        except Exception as e:
            print(f"Error reading {args.file}: {e}")
            print("**FINAL OUTPUT**")
            return
    else:
        print("Error: Please provide domains or a file path.")
        print("**FINAL OUTPUT**")
        return

    # 2. Parallel lookups with rate limiting
    domain_queue = queue.Queue()
    for domain in domains:
        domain_queue.put(domain)

    results = []
    num_threads = 10  # Adjust as needed
    
    for _ in range(num_threads):
        thread = threading.Thread(target=lookup_registrar, args=(domain_queue, results))
        thread.daemon = True  # Daemonize thread
        thread.start()

    domain_queue.join()  # Wait for all domains to be processed

    # 3. Output results
    df_results = pd.DataFrame(results)

    if args.format == 'csv':
        output = df_results.to_csv(index=False)
    elif args.format == 'json':
        output = df_results.to_json(orient='records')
    else:  # text
        output = ""
        for _, row in df_results.iterrows():
            output += f"Domain: {row['domain']}, Registrar: {row['registrar']}\n"

    print("**FINAL OUTPUT**")
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Results saved to {args.output}")
        except Exception as e:
            print(f"Error writing to {args.output}: {e}")
    else:
        print(output)


if __name__ == "__main__":
    main()

# Note: Be respectful of the whois server's rate limits and usage policies.

# usage:
# 1. Provide domains as command line arguments: python whois-utility.py example.com openai.com
# 2. Or, provide a file path: python whois-utility.py --file domains.csv
# 3. The results will be printed to stdout or saved to a file specified by --output