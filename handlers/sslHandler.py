import urllib3
import certifi

def has_valid_ssl(domain):
    try:
        http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
        response = http.request('GET', domain)
        if response.status == 200:
            return True
        else:
            return False

    except Exception as e:
        return False
        
