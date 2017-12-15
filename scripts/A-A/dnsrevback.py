#!/usr/bin/env python
import dns.resolver
import dns.reversename
import sys

domains = set()
for line in sys.stdin:
	domain = line.strip()

	try:
		ipv4 = map(str, dns.resolver.query(domain, "A"))
	except:
		ipv4 = []

	try:
		ipv6 = map(str, dns.resolver.query(domain, "AAAA"))
	except:
		ipv6 = []

	rev_domains = map(dns.reversename.from_address, ipv4 + ipv6)
	rev_domains = map(str, rev_domains)

	def getrev(d):
		try:
			return list(dns.resolver.query(d, "PTR"))
		except:
			return []

	rev_domains = map(getrev, rev_domains)

	for rev_domain in rev_domains:
		for d in rev_domain:
			domain = str(d)
			if domain[-1] == ".": domain = domain[:-1]
			domains.add( domain )

	try:
		domains.remove(domain)
	except KeyError:
		pass

print "\n".join(list(domains))