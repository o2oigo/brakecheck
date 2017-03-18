#!/usr/bin/python

import adtools
import argparse

def main():
    # Parse input arguments
    parser = argparse.ArgumentParser(description='BrakeCheck applies network policies via a pf or a pfSense \
                                                firewall. These policies are based on a user\'s Active Directory \
                                                account and their corresponding group(s).')
    parser.add_argument('-u','--username', help='Active Directory username')
    parser.add_argument('-d','--domain', help='Active Directory domain')
    parser.add_argument('-p','--password', help='Active Directory password')
    parser.add_argument('-a','--ipaddress', help='Active Directory host ip address')
    parser.add_argument('-s','--search', help='Active Directory user to search for.')
    args = parser.parse_args()

    if (args.username == None) or (args.domain == None) or (args.password == None) or (args.ipaddress == None):
        print 'Could not connect to AD server. Not all login credentials specified!'
        exit()

    # Create a connection to AD server
    conn = adtools.Connection(args.ipaddress, args.username + '@' + args.domain, args.password)
    print conn.search(args.search)
    conn.close()

if __name__ == '__main__':
    main()
