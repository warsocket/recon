#!/usr/bin/env python
import requests
import sys

domains = set()
for line in sys.stdin:
    domain = line.strip()
    certs = requests.get("https://certspotter.com/api/v0/certs?domain=%s" % domain).json()

    try:
        for cert in certs:
            for domain in cert["dns_names"]:
                domain = domain.replace("*.", "")
                domains.add(domain)
    except:
        pass

for d in domains:
    print d
