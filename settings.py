from apns import APNs

#apns = APNs(use_sandbox=True, cert_file='certs/bunker1cc_apns.pem', key_file='certs/bunker1cc_apns.pem')
apns = APNs(use_sandbox=False, cert_file='certs/bunker1cc_apns_dist.pem', key_file='certs/bunker1cc_apns_dist.pem')

