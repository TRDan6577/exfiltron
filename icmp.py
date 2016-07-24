"""
* imcp.py
*
*
"""

from scapy.all import*
import os
import sys

#  icmp: args: destinationIP(string), filename(str), BytesPerPacket(int)
#  rtn: list of packets

def icmp(destIP, filename, BytesPP):
    READ_ONLY = 'r'
    listOfPackets = []
    size = 0
    numPackets=0
    dataPP=BytesPP-1

   
    # size is the number of bytes in the file
    try:
        size=os.stat(filename).st_size
    except LookupError:
        print("Could not find " + filename)
        print("Exiting...")
        sys.exit()
    
    #if size > 
    # the number of packets send should be the size of the
    # file divided by the number of bytes per packet
    numPackets = size/BytesPP 
    
  
    # opening the specified file **needs error handling**
    OFile = open(filename, READ_ONLY)  
 
    #need to work on the for loop
    for i in range(numPackets):
        partOfFile=OFile.read(dataPP)
        data = str(i) + partOfFile
        packet=sr(IP(dst=destIP)/ICMP()/partOfFile)
        print(i)
    
    
    file.close()
