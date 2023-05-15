from ssl import CertificateError
import urllib3


def has_valid_ssl(domain):
    try:
        http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=CertificateError.where()
    )
        
        response = http.request('GET', domain)
        if response.status == 200:
            return True
        else:
            return False

    except urllib3.exceptions.SSLError:
        return False
    except urllib3.exceptions.HTTPError:
        return False
    except urllib3.exceptions.RequestError:
        return False
