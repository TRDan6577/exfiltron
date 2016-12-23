"""
File: encryption.py
Purpose: Holds all of exfiltron's cryptographic functions
Author: Thomas Daniels
"""

import os       # PRNG
import sys      # sys.exit(), platform specific commands
import getpass  # User entering the key/IV


# Make sure the cryptography package is installed
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("Could not import cryptography. Please make sure it's installed.")
    print("Exiting...")
    sys.exit()


def encrypt(data):
    """
    Purpose: Encrypts the given data with AES-256 and CTR mode
    @param (bits) data - arbitrary data to encrypt
    @return (bits) the encrypted data
    """

    sameKey = False
    while(not sameKey):
        # Get the key from the user
        key = getpass.getpass("Please enter the key you wish to use to encrypt " +
                    "the data (the key you enter will be hashed using SHA-256. If" +
                    " you leave this field blank, the OS will generate a random " +
                    "cryptographically secure number for you to use as the key. " +
                    "This key will be printed to stdout so that you can use it " +
                    "for the decryption on the server (attacker) side): ")

        # No need to check key if user wants random key
        if(key is ''):
            break

        # Confirm the key
        confirm_key = getpass.getpass("Please confirm key: ")
        sameKey = confirm_key is key

    # Get the IV from the user
    IV = raw_input("Please enter the initalization vector to be used in CTR" +
                " mode. The IV should NEVER be reused and should be a nonce." +
                " (If you leave this field blank, the OS will generate a " +
                "random cryptographically secure number for you to use as " +
                "the IV. The IV will be printed to stdout so that you can " +
                "use it for the decryption on the server (attacker) side): ")

    # If the user didn't enter anything, generate a random 256 bit key
    if(key is ''):
        
        # Pick a random number for the key
        key = os.urandom(32)

        # Get terminal ready to display the key. Start by clearing the screen
        if(sys.platform.startswith('win')):
            os.system("cls")
        else:
            os.system("clear")

        # Print the key
        print("Once you have the key written down/copied to your clipboard, " +
              "press 'Enter' to overwrite the key with whitespace. The key " +
              "will be represented as a hex string.")
        sys.stdout.write("Key: ")
        sys.stdout.flush()
        "".join("{:02x}".format(ord(c)) for c in key)

        # Wait for input
        raw_input("")

        # Overwrite key with whitespace (Shout out to Nick K. on stackoverflow)
        print('\033[{0}D\033[2A'.format(len(key)) + 
            " "*(len(key)*2 + len("Key: ")))
    else:
        # Take their input and shove it through SHA-256 to get a key of the
        # appropriate size
        from cryptography.hazmat.primitives import hashes
        digest = hashes.Hash(hashes.SHA256(), default_backend())
        digest.update(key)
        key = digest.finalize()

    # If no IV was entered, generate a random one and show it to the user
    # Note that the IV does NOT need to be kept a secret
    if(IV = ''):
        IV = os.urandom(16)
        
        sys.stdout.write("Your IV is: ")
        sys.stdout.flush()
        "".join("{:02x}".format(ord(c)) for c in IV)
    else:
        # Take their input and find the MD5 hash of it to get an IV of
        # the appropriate size (need IV of 128 bits/16 bytes)
        from cryptography.hazmat.primitives import hashes
        digest = hashes.Hash(hashes.MD5(), default_backend())
        digest.update(IV)
        IV = digest.finalize()

    # Make the cipher
    cipher = Cipher(algorithms.AES(key), modes.CTR(IV), default_backend())
    encryptor = cipher.encryptor()
    
    # Return the ciphertext
    return (encryptor.update(data) + encryptor.finalize())

def decrypt(data):
    """
    Purpose: decrypts the given data
    @param (bits) data - the ciphertext
    @return (bits) the plaintext
    """

    # Determine the key
    sameKey = False
    while(not sameKey):
        # Get the key from the user
        print("Please enter the key you used to encrypt the data on the " +
              "client (target) side. IF YOU HAD EXFILTRON GENERATE THE KEY " +
              "FOR YOU, LEAVE THIS FIELD BLANK AND JUST PRESS ENTER")
        key = getpass.getpass("Key: ")

        # Get hex version of randomly generated key from the user
        if(key is ''):
            break

        # Confirm the key
        confirm_key = getpass.getpass("Please confirm key: ")
        sameKey = confirm_key is key
    

    # If we generated the key, we'll need to convert from string to bytes
    if(key = ''):
        sameKey = False
        while(not sameKey):
            # Get the key from the user
            print("Please enter the hex version of the key Exfiltron " +
                  "generated for you")
            hexInput = getpass.getpass("Key: ")

            # Confirm the key
            confirm_key = getpass.getpass("Please confirm key: ")
            sameKey = confirm_key is hexInput

        key = hexInput.decode('hex')
    else:
        # Hash the user given key so that it's length is 256 (using SHA256...)
        from cryptography.hazmat.primitives import hashes
        digest = hashes.Hash(hashes.SHA256(), default_backend())
        digest.update(key)
        key = digest.finalize()


    # Get the IV from the user
    print("Please enter the IV you used to encrypt the data on the " +
          "client (target) side. IF YOU HAD EXFILTRON GENERATE THE IV " +
          "FOR YOU, LEAVE THIS FIELD BLANK AND JUST PRESS ENTER")
    IV = raw_input("IV: ")

    # If Exfiltron generated one for the user, convert it to bytes
    if(IV = ''):
        print("Please enter the hex version of the IV Exfiltron generated for" +
              " you")
        IV = raw_input("IV: ")
        IV = IV.decode('hex')
    else:
        from cryptography.hazmat.primitives import hashes
        digest = hashes.Hash(hashes.MD5(), default_backend())
        digest.update(IV)
        IV = digest.finalize()

    # Make the cipher
    cipher = Cipher(algorithms.AES(key), modes.CTR(IV), default_backend())
    decryptor = cipher.decryptor()
    
    # Return the ciphertext
    return (decryptor.update(data) + decryptor.finalize())

