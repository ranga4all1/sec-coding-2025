# Whois Lookup Script 

# python script that calls a whois server to lookup the registrar of a list of domains

# install the required package
# ! pip install python-whois


import whois
import pandas as pd

def lookup_registrar(domains):
    results = []
    for domain in domains:
        try:
            w = whois.whois(domain)
            registrar = getattr(w, 'registrar', 'Not found')
            results.append({'domain': domain, 'registrar': registrar})
        except Exception as e:
            results.append({'domain': domain, 'registrar': f'Error: {e}'})
    return results

# Example usage
# sample_domains = ['google.com', 'wikipedia.org', 'python.org']
# lookup_results = lookup_registrar(sample_domains)
# pd.DataFrame(lookup_results).to_csv('whois_registrars_python.csv', index=False)

