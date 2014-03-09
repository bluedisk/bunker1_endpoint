# -*- coding: utf-8 -*-

from apns import APNs,Payload



apns = APNs(use_sandbox=True, cert_file='certs/bunker1cc_apns.pem', key_file='certs/bunker1cc_apns.pem')
#apns = APNs(use_sandbox=False, cert_file='certs/bunker1cc_apns_dist.pem', key_file='certs/bunker1cc_apns_dist.pem')

payload = Payload(alert='TEST MESSAGE', sound="default", badge=1)

token = 'df35f21dc46b5d464a16f9c3e6f818cdd5c37f43cccc25f07d00d760ac3625c1'
#token = '76aa2f1bd2032df3350f666799d5f5239792922c80e3f3f78e14e580ef7be24a'
apns.gateway_server.send(token, payload)

	


