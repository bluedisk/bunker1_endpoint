from apns import APNs

APNS_SANDBOX=False
APNS_CERT='certs/bunker1cc_apns_dist.pem'

def connectToAPNS():
    return APNs(use_sandbox=APNS_SANDBOX, cert_file=APNS_CERT, key_file=APNS_CERT)

