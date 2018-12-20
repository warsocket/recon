#!/usr/bin/env python
import requests
import re
import sys

TABLE_PARSE_REGEX = "\s+<TR>\s*(<TD[^>]*>[\s\S]*?</TD>)*\s*</TR>"

def get_and_parse_ct(domain, wildcard = False):
    cts = { 
        False: "https://crt.sh?q={}",
        True: "https://crt.sh?q=%25.{}"
    }

    ct_url = cts[wildcard].format(domain)

    def parse_regex_output(found_elem):
        return filter(lambda x: x, map(lambda s: s.strip()[1:-1].split(">")[-1].split("<")[0], found_elem.group(1).split("\n"))) + ([domain] if not wildcard else [])

    ret = requests.get(ct_url)
    return map(parse_regex_output, re.finditer(TABLE_PARSE_REGEX, ret.text))

def getct(domain):
    return get_and_parse_ct(domain) + get_and_parse_ct(domain, True)

domains = set()
for line in sys.stdin:
    domain = line.strip()
    for _,_,_,d in getct(domain):
        domains.add(d.replace("*.", ""))
        
for d in domains:
    print d