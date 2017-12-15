#!/usr/bin/env python
DEBUG=False

import sys
import os
import argparse
import re
import json
import subprocess
import operator

#init stuffs
regex_a = re.compile("^(?!\-)(?:[a-zA-Z\d\-]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z\d]{1,63}$")
regex_ip = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")

class Script():
	def __init__(self, scripttype, scriptname, scriptpath):
		self.__type = scripttype
		self.__name = scriptname
		self.__path = scriptpath

	def get_type(self):
		return self.__type

	def get_name(self):
		return self.__name

	def get_path(self):
		return self.__path

	def run(self, args): #Runs thhis instance of this script in recon
		typestring = self.__type[:]
		typestring = typestring.replace("_", " ")
		typestring = typestring.replace("-", " -> ")
		print >> sys.stderr, "\tRunning script %s (%s): " % (self.__name, typestring) , 

		if self.__type in ["A-IP", "A-A"]:
			inputstring  = "\n".join(worksetA)

		elif self.__type in ["IP-IP", "IP-A"]:
			inputstring  = "\n".join(worksetIP)

		elif self.__type in ["FILTER_A"]:
			inputstring  = "\n".join(knownsetA)

		elif self.__type in ["FILTER_IP"]:
			inputstring  = "\n".join(knownsetIP)

		try:
			is_filter = (self.__type.find("FILTER")  >= 0 )
			# print inputstring

			p = subprocess.Popen([self.__path] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stdout, stderr = p.communicate(input=inputstring)

			print >> sys.stderr, ["OK", "FAIL"][bool(p.returncode)], "(%s)" % p.returncode,

			print >> sys.stderr, " # %d -> %d" % (len(inputstring.split("\n")), len(set(stdout.split("\n"))))
		except:
			print >> sys.stderr, "\n\t\tError while running tool %s (%s)" % (self.__name, self.__path)
			if DEBUG: print >> sys.stderr, stderr
			stdout = ""

		if self.__type in ["IP-A", "A-A", "FILTER_A"]:
			for line in stdout.split():
				domain = line.strip()
				if domain[-1] == ".": domain = domain[:-1]
				if not regex_a.match(domain):
					print >> sys.stderr, "\t\tRejecting invalid domain '%s'" % domain
				else:
					if is_filter:
						if domain in knownsetA: worksetA.add(domain)
					else:
						knownsetA.add(domain)

		elif self.__type in ["A-IP", "IP-IP", "FILTER_IP"]:
			for line in stdout.split():
				ip = line.strip()
				if not regex_ip.match(ip):
					print >> sys.stderr, "\t\tRejecting invalid IP '%s'" % ip
				else:
					if is_filter:
						if ip in knownsetIP: worksetIP.add(ip)
					else:
						knownsetIP.add(ip)



#parse stuffs
parser = argparse.ArgumentParser(description='Recon front door sevices')
parser.add_argument('scripts', type=str, nargs='*', help='Recon scripts to run')
parser.add_argument('--a', type=str, nargs='*', help='Seed the engine with A-records')
parser.add_argument('--ip', type=str, nargs='*', help='Seed the engine with IP\'s')
parser.add_argument('--list', action="store_true", help='List all available scripts after parsing')
parser.add_argument('--emit-a', action="store_true", default=False, help='Emit A records in working set, if --emit-ip is also omitted both will be emitted.')
parser.add_argument('--emit-ip', action="store_true", default=False, help='Emite IP record in working set if --emit-a is also omitted both will be emitted.')
args = parser.parse_args()

#validate input
if args.a == None: args.a = []
for a in args.a:
	if not regex_a.match(a):
		print >> sys.stderr, "Invalid domain name: %s" % a
		exit(1)

if args.ip == None: args.ip = []
for ip in args.ip:
	if not regex_ip.match(ip):
		print >> sys.stderr, "Invalid IP: %s" % ip
		exit(1)



print >> sys.stderr, "Starting..."


print >> sys.stderr, "Parsing scripts..."
scriptdir = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "scripts")
scripttypes = set(["A-IP", "A-A", "IP-A", "IP-IP", "FILTER_A", "FILTER_IP"])

def make_scripts(scriptsubdir): #create recon script objects from a directory
	subdir = os.path.join(scriptdir, scriptsubdir)
	files = filter(lambda f: os.path.isfile( os.path.join(subdir, f) ), os.listdir(subdir))

	#Ignore pyc files and symlinks
	ignore = [".pyc"]
	files = filter( lambda f: not(reduce(operator.__or__, map(f.endswith, ignore))), files) # filter out filestypes in ignore list
	files = filter( lambda f: not(os.path.islink(os.path.join(subdir, f))), files ) # filter out symlink files
	return map( lambda f: Script( *(scriptsubdir, f.split(".", 1)[0], os.path.join(subdir, f)) ), files ) #make them into objects


scriptmap = {}
for script in sum(map(make_scripts, scripttypes), []):
	name = script.get_name()

	if name in scriptmap:
		print >> sys.stderr, "Ambiguous script name reference: %s" % name
		exit(1)

	scriptmap[name] = script


print >> sys.stderr, "Checking requested scripts for existence..."
for scriptname in args.scripts:
	scriptname = scriptname.split()[0]
	if scriptname not in scriptmap:
		print >> sys.stderr, "Script %s not found" % scriptname
		exit(1)

if args.list:
	scripts = map( lambda s: (s.get_type(), s.get_name()), scriptmap.values() )
	displaymap = {}
	for scripttype, scriptname in scripts:
		if scripttype not in displaymap:
			displaymap[scripttype] = []
		displaymap[scripttype].append(scriptname)

	for key in displaymap.keys():
		print "%s:" % key
		for scriptname in sorted(displaymap[key]):
			try:
				with open( os.path.join(scriptdir, "doc", "%s.txt" % scriptname), "r" ) as f:
					message = f.read()
			except:
				message = "No documentation found."
			print "|%s|" % scriptname, message
		print ""

	exit(0)


#Main starts here (ex: argument- and sctript parsing)
print >> sys.stderr, "Running scripts..."
worksetA = set(args.a)
worksetIP = set(args.ip)

knownsetA = set(args.a)
knownsetIP = set(args.ip)

for scripttarget in args.scripts:
	split = scripttarget.split()
	script = split[0]
	scriptargs = split[1:]
	scriptmap[script].run(scriptargs)


if not(args.emit_a | args.emit_ip):
	args.emit_a = True
	args.emit_ip = True

if args.emit_a:
	print "\n".join(worksetA)
if (args.emit_a & args.emit_ip):
	print ""
if args.emit_ip:
	print "\n".join(worksetIP)