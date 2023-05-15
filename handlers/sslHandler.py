import urllib3
import certifi

def has_valid_ssl(domain):
    try:
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )

        response = http.request('GET', domain)
        if response.status == 200:
            print("200:")
            return True
        else:
            print("else:")
            return False

    except urllib3.exceptions.SSLError:
        print("SSLError:")
        return False
    except urllib3.exceptions.HTTPError as e:
        print("HTTPError:", e)
        return False
    except urllib3.exceptions.RequestError:
        print("RequestError:")
        return False