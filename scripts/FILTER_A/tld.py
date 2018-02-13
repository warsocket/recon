#!/usr/bin/env python
import sys
import re
import operator
import sys
import reconutil

whitelist = sys.argv[1:]

for line in sys.stdin:
    subdomain = line.strip()

    if reduce(operator.__or__, map(lambda d: reconutil.is_subdomain(d, subdomain), whitelist), False):
        print subdomain
