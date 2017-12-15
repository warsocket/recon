#!/usr/bin/env python
import sys
import reconutil
whitelist = sys.argv[1:]

checked_yes = set()
checked_no = set()

ranges = []
for line in sys.stdin:
	ip = line.strip()

	if ip in checked_no:
		continue

	if ip in checked_yes:
		print ip
		continue

	whois = reconutil.get_whois(ip)
	# check for @tld abuse address
	
	try:
		tld = reconutil.get_whois_abuse(whois)
	except:
		continue
	
	#get the whole range
	checked = set()
	r = reconutil.get_whois_range(whois)
	for ip in reconutil.whois_range_to_ips(r):
		checked.add(ip)

	#Addrange to correct set

	if tld in whitelist: #positive hit
		checked_yes |= checked
		print ip
	else: #negative hit
		checked_no |= checked
