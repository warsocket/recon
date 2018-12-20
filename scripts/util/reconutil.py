import re
import subprocess
import struct

range_regex = re.compile("\w:\s*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ - [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)")
abusetld_regex = re.compile("((abuse-mailbox)|(OrgAbuseEmail)):\s+.*@(.*)")


def is_subdomain(domain, subdomain):
    return bool(re.match("(.+\\.)?%s$" % domain.replace(".", "\\."), subdomain))


def get_whois(ip):
    assert(re.match("""[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+""", ip))  # refuing command injection
    return subprocess.check_output(["/usr/bin/whois", ip])


def get_whois_range(whois):
    return range_regex.search(whois).group(1)


def get_whois_abuse(whois):
    return abusetld_regex.search(whois).group(4)


def whois_range_to_ips(whoisrange):
    ips = []

    left, right = whoisrange.split("-")
    left = left.strip()
    right = right.strip()

    begin = map(int, left.split("."))
    end = map(int, right.split("."))

    sint_begin = struct.unpack("!L", struct.pack("!BBBB", *begin))[0]  # convert ip to single 32-bit number
    sint_end = struct.unpack("!L", struct.pack("!BBBB", *end))[0]  # convert ip to single 32-bit number

    for sip in range(sint_begin, sint_end + 1):
        ips.append(".".join(map(str, struct.unpack("!BBBB", struct.pack("!L", sip)))))

    return ips
