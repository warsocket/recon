#!/usr/bin/env python
import dns.resolver
import sys

ips = set()

for line in sys.stdin:
    domain = line.strip()

    try:
        ipv4 = map(str, dns.resolver.query(domain, "A"))
        ips |= set(ipv4)
    except:
        pass


print "\n".join(list(ips))
