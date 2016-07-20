"""
File: exfiltron.py
Author: Thomas DAniels
Purpose: This is the main running program for the Exfiltron framework. This 
        program is used as a prompt for the attacker to execute his or her
        desired commands using other parts of this framework.
"""

try:
    from scapy.all import *  # Use the almighty scapy package
except ImportError:          # Raise an error if scapy is not installed
    print("Could not import scapy. Is it installed?")
    SystemExit()

import argparse              # For parsing command line arguments


"""
Purpose: Parses the command line args and sends them back to main for
        interpretation
@param (NoneType) None
@return (List) a list of parsed arguments to interpret
"""
def setArgParserOptions():
    parser = argparse.ArgumentParser(description='
     ####### ##  ## ####### #### ####   ###### ######   #####  ##   ## 
      ##   # ##  ##  ##   #  ##   ##    # ## #  ##  ## ##   ## ###  ## 
      ## #    ####   ## #    ##   ##      ##    ##  ## ##   ## #### ## 
      ####     ##    ####    ##   ##      ##    #####  ##   ## ## #### 
      ## #    ####   ## #    ##   ##   #  ##    ## ##  ##   ## ##  ### 
      ##   # ##  ##  ##      ##   ##  ##  ##    ##  ## ##   ## ##   ## 
     ####### ##  ## ####    #### ####### ####  #### ##  #####  ##   ##

     Exfiltron is a data exfiltration framework designed to help you get data
     off of a machine without tripping an IDS or alerting a systems
     administrator.', prog='exfiltron.py')

    parser.add_argument('exfiltrate', metavar='method', type=string,
                        action='store_true', dest='method', help=("This is" +
                        " the method of exfiltration. Your options are: icmp"))

    parser.add_argument('-f', '--file-name', metavar='-f', type=string,
                        action='store_true', dest='file', help=("The name of" +
                        " the file you wish to.. *ahem*... 'borrow'"))

    parser.add_argument('-d', '-dest-ip', metavar='-d', type=string,
                        action='store_true', dest='destIP', help=("The IP " +
                        "address you want the data sent to"))

    parser.add_argument('-s', '--source-IP', metavar='[-s]', type=string,
                        action='store_true', dest='srcIP', help=("The spoofed" +
                        " IP address you want the data sent from. By default" +
                        ", the data is sent from the actual IP. Use this " +
                        "with caution. This may set off an alarm if the " +
                        "network is using DHCP snooping"))

    parser.add_argument('-a', '--data-per-packet', metavar='[-a]', type=int,
                        action='store_true', dest='amountOfData', help=("By" +
                        " default, the amount of data stored in a packet is" +
                        " the same as it normally is to decrease the chances" +
                        " of detection by an IDS (example: ICMP exfiltration" +
                        " will have a default packet size of 64 bytes). Use" +
                        " this option to send more or less data"))

    return parser.parse_args()


def main():
    # Parse the commands from the command line with argparser
    args = setArgParserOptions()
