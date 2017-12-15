#!/usr/bin/env python
import sys
import reconutil

ranges = []
for line in sys.stdin:
	ip = line.strip()

	whois = reconutil.get_whois(ip)
	r = reconutil.get_whois_range(whois)
	print "\n".join(reconutil.whois_range_to_ips(r))


