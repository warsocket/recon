#!/usr/bin/env python
import dns.resolver
import dns.reversename
import sys

domains = set()
ips = set()

for line in sys.stdin:
	ip = line.strip()

	rev_domain = dns.reversename.from_address(ip)
	
	try:
		 map(domains.add, map(str, list(dns.resolver.query(rev_domain, "PTR"))) )
	except:
		pass

print "\n".join(list(domains))