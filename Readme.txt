Recon: A scriptable reconnaissance engine.


Workings:

Recon is an engine in which you chain various scripts that have interface [IP/A] -> [IP/A].
The input is written to the STDIN of the script and the OUTPUT read form the STDOUT, IP'a and A records are delimited by newlines.

You can run a number of scripts to generate 'candidate' results which get imported back in the main result set trough the use of filters.
YOu can seed your working set with the --a and --ip flags accordingly

Examples:
I can write a whole paper about the internal workings but examples will give you more insight with less text.

./recon.py resolv ip --a example.com
resolves example.com and adds the ip(s) to the working set

./recon.py ct a --a example.com example.org
Get certificates trough CT of example.com and example.org and add them to working set

./recon.py getrange publicip reverse a --ip 31.13.64.35 --emit-a
Get the range wherein 31.13.64.35(facebook ip) resides and thereafter do a reverse lookup on all those ip's. Then emit the found dns names


CT script:
Please note that using this script is subject to the terms and conditions of the endpoint used within: (https://certspotter.com/api/v0/certs)