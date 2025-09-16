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
                finally:
                    pass # No action needed here
            domain_queue.task_done()
        except queue.Empty:
            break

def main():
    # 1. Read domains from CSV file
    try:
        domains_df = pd.read_csv('domains.csv', header=None, names=['domain'], dtype={'domain': str})
        domains_df = domains_df.dropna()  # Remove rows with NaN values
        domains = domains_df['domain'].tolist()
        domains = [d.strip() for d in domains] # Remove whitespace
    except FileNotFoundError:
        print("Error: domains.csv not found.  Please create a CSV file named domains.csv with a list of domains in the first column.")
        return
    except Exception as e:
        print(f"Error reading domains.csv: {e}")
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

    # 3. Output results to CSV
    pd.DataFrame(results).to_csv('whois_registrars_threaded.csv', index=False)
    print("Results saved to whois_registrars_threaded.csv")

if __name__ == "__main__":
    main()

# Note: Be respectful of the whois server's rate limits and usage policies.

# usage:
# 1. Create a CSV file named domains.csv with a list of domains in the first column.
# 2. Run the script: python whois-utility.py
# 3. The results will be saved to whois_registrars_threaded.csv