from apns import APNs
from pygcm.manage import GCMManager
from certs.gcm import GCM_KEY

APNS_SANDBOX=False
APNS_CERT='certs/bunker1cc_apns_dist.pem'

def connectToAPNS():
    return APNs(use_sandbox=APNS_SANDBOX, cert_file=APNS_CERT, key_file=APNS_CERT)

def connectToGCM():
    return GCMManager(GCM_KEY)