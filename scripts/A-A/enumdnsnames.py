#!/usr/bin/env python
import dns.resolver
import re
import sys

DOMAIN_REGEX = """((\w|-)+\.)+(\w|-)+"""
m = re.compile(DOMAIN_REGEX)

domains = set()

for line in sys.stdin:
	domain = line.strip()
	print domain

	for x in range(1, 0x80):
		try:
			answers = dns.resolver.query(domain, x)
			for answer in answers:
				ans = str(answer)
				ans = ans.replace("=", " ")
				ans = ans.replace(":", " ")

				l = filter( lambda x: m.match(x), ans.split() )
				for x in l:
					domains.add(x)

		except dns.resolver.NoAnswer:
			pass

		except dns.resolver.NoMetaqueries:
			pass

		except dns.resolver.NoNameservers:
			pass

		except dns.exception.Timeout:
			pass

		except dns.resolver.NXDOMAIN:
			pass


print "\n".join(domains)