"""
File: exfiltron.py
Author: Thomas DAniels
Purpose: This is the main running program for the Exfiltron framework. This 
        program is used as a prompt for the attacker to execute his or her
        desired commands using other parts of this framework.
"""


import argparse     # For parsing command line arguments
import logging      # Get rid of that pesky scapy IPv6 warning
import sys          # If unexpected results occur, stop usage (and call your doctor)

try:
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    from scapy.all import *  # Use the almighty scapy package
except ImportError:          # Raise an error if scapy is not installed
    print("Could not import scapy. Is it installed? Are you running python2?")
    print("Exiting...")
    sys.exit()

"""
Purpose: Parses the command line args and sends them back to main for
        interpretation
@param (NoneType) None
@return (List) a list of parsed arguments to interpret
"""
def setArgParserOptions():
    # Create the argument parser
    parser = argparse.ArgumentParser(formatter_class=
                                     argparse.RawDescriptionHelpFormatter,description=('' +
     '####### ##  ## ####### #### ####   ###### ######   #####  ##   ##\n' +
     ' ##   # ##  ##  ##   #  ##   ##    # ## #  ##  ## ##   ## ###  ##\n' +
     ' ## #    ####   ## #    ##   ##      ##    ##  ## ##   ## #### ##\n' +
     ' ####     ##    ####    ##   ##      ##    #####  ##   ## ## ####\n' +
     ' ## #    ####   ## #    ##   ##   #  ##    ## ##  ##   ## ##  ###\n' +
     ' ##   # ##  ##  ##      ##   ##  ##  ##    ##  ## ##   ## ##   ##\n' +
     '####### ##  ## ####    #### ####### ####  #### ##  #####  ##   ##\n' +

     '\nExfiltron is a data exfiltration framework designed to help you get' +
     ' data off of a machine without tripping an IDS or alerting a system' +
     ' administrator.'), prog='exfiltron.py')

    # Add the method of exfiltration option
    parser.add_argument('method', type=str, help=('This is the method of ' +
                        'exfiltration. Your options are: icmp'))

    # Add the file name option
    parser.add_argument('-f', '--file-name', type=str, help=("The name of" +
                        " the file you wish to.. *ahem*... 'borrow'"),
                        required=True)

    # Add the destination IP address option
    parser.add_argument('-d', '--dest-ip', type=str, help=("The IP " +
                        "address you want the data sent to. Please note " +
                        "that this option is required"), required=True)

    # Add the source IP optional argument
    parser.add_argument('-s', '--source-IP', type=str,
                        help=("The spoofed IP address you want the data sent" +
                        " from. By default, the data is sent from the actual" +
                        "IP address of the machine you're on. Please note " +
                        "that this option is required"))

    # Add the data per packet optional argument
    parser.add_argument('-a', '--data-per-packet', type=int,
                        help=("By default, the amount of data stored in a " +
                        "packet is the same as it normally is to decrease " +
                        "the chances of detection by an IDS (example: ICMP" +
                        "exfiltration will have a default packet size of " +
                        "64 bytes). Use this option to send more or less data"))

    return parser.parse_args()


def main():
    # Parse the commands from the command line with argparser
    args = setArgParserOptions()

if (__name__ == '__main__'):
    main()
