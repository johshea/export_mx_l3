#!/usr/bin/python3

READ_ME = '''
=== PREREQUISITES ===
Run in Python 3 with Meraki dashboard API Python library @
https://github.com/meraki/dashboard-api-python/
pip[3] install --upgrade meraki


=== DESCRIPTION ===
Exports CSV of MX L3 outbound firewall rules.

=== USAGE ===
python[3] export_mx_l3.py [-k <api_key>] -n <net_id>

API key can also be exported as an environment variable named
MERAKI_DASHBOARD_API_KEY
'''


import csv
from datetime import datetime
import getopt
import os
import sys
import meraki
from pathlib import Path



# Prints READ_ME help message for user to read
def print_help():
    lines = READ_ME.split('\n')
    for line in lines:
        print('# {0}'.format(line))


def main(argv):
    # Set default values for command line arguments
    api_key = net_id = None

    # Get command line arguments
    try:
        opts, args = getopt.getopt(argv, 'h:k:n:')
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt == '-k':
            api_key = arg
        elif opt == '-n':
            net_id = arg

    # Check if all required parameters have been input
    if (api_key == None and os.getenv('MERAKI_DASHBOARD_API_KEY') == None) or net_id == None:
        print_help()
        sys.exit(2)

    # Set the CSV output file and write the header rowappliance.getNetworkApplianceFirewallL3FirewallRules
    time_now = f'{datetime.now():%Y-%m-%d_%H-%M-%S}'


    # Dashboard API library class
    m = meraki.DashboardAPI(api_key=api_key, log_file_prefix=__file__[:-3])

    # Read configuration of MX L3 firewall rules
    fw_rules = m.appliance.getNetworkApplianceFirewallL3FirewallRules(net_id)

    #Create an Empty list to store rows
    fw_rule_df = []
    for key, value in fw_rules.items():
        for i in range(len(value)):
            fw_rule_data = {'policy': value[i]['policy'], 'protocol': value[i]['protocol'], 'srcCidr': value[i]['srcCidr'], 'srcPort': value[i]['srcPort'], 'destCidr': value[i]['destCidr'], 'destPort': value[i]['destPort'], 'comment': value[i]['comment'], 'syslogEnabled': value[i]['syslogEnabled']}
            #print(fw_rule_data)
            fw_rule_df.append(fw_rule_data)

    # Create and write the CSV file (Windows, linux, macos)
    if len(fw_rule_df) > 0:
        keys = fw_rule_df[0].keys()
        file_name = f'mx_l3fw_rules_{net_id}-{time_now}.csv'
        inpath = Path.cwd() / file_name
        with inpath.open(mode='w+', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(fw_rule_df)

    print("Firewall rules for NetworkId: " + net_id + " downloaded.")









if __name__ == '__main__':
    main(sys.argv[1:])
