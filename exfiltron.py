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

    return parser.parse_args()


def main():
    # Parse the commands from the command line with argparser
    args = setArgParserOptions()
