##!/usr/bin/env python3

import argparse
import ipaddress
from termcolor import colored as color

banner = color(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
███████╗███╗   ██╗███████╗████████╗██╗███╗   ██╗███████╗ ██████╗ 
██╔════╝████╗  ██║██╔════╝╚══██╔══╝██║████╗  ██║██╔════╝██╔═══██╗
███████╗██╔██╗ ██║█████╗     ██║   ██║██╔██╗ ██║█████╗  ██║   ██║
╚════██║██║╚██╗██║██╔══╝     ██║   ██║██║╚██╗██║██╔══╝  ██║   ██║
███████║██║ ╚████║███████╗   ██║   ██║██║ ╚████║██║     ╚██████╔╝
╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            Get Subnetting Information quickly!!

""", "cyan")


def main():
    class CustomHelpFormatter(argparse.HelpFormatter):
        def add_usage(self, usage, actions, groups, prefix=None):
            if prefix is None:
                prefix = color('usage: ', "yellow")
            return super(CustomHelpFormatter, self).add_usage(usage, actions, groups, prefix)

        def format_help(self):
            return banner + super(CustomHelpFormatter, self).format_help()

    #Create arguments analyzer
    parser =  argparse.ArgumentParser(
        description=color('Calculate Network ID and Broadcast Address', 'yellow'),
        epilog=color('Example: python subnetting_calc.py 192.168.13.12/24', 'yellow'),
        formatter_class=CustomHelpFormatter
        )
    parser.add_argument('ip', type=str, help=color('IP address with CIDR prefix (Ex. 192.168.13.12/24)', 'yellow'))

    #Parse the arguments
    args = parser.parse_args()

    #Convert the IP and CIDR prefix to a network interface
    ip = ipaddress.ip_interface(args.ip)
    ip_address = args.ip.split('/')[0]
    network = ip.network
    mask =  network.netmask

    def calculate_host(network):
        total_ips = network.num_addresses
        usable_hosts = total_ips - 2

        if network.prefixlen == 31:
            usable_hosts = 2
        elif network.prefixlen == 32:
            usable_hosts = 1

        return total_ips, usable_hosts

    host = calculate_host(network)
    print(host)
    #Calculate Network ID and Broadcast Mask
    network_id = network.network_address
    broadcast_address = network.broadcast_address


    #Show results
    print(banner)
    print(color(f"╔════════════════════════════════════════╗", 'yellow'))
    print(color(f"║ [+] Address: {network_id}              ║", 'green'))
    print(color(f"║ [+] NetMask: {mask}             ║", 'green'))
    print(color(f"║ [+] Network: {network_id}/{network.prefixlen}           ║", 'cyan'))
    print(color(f"║ [+] Broadcast Address: {broadcast_address}  ║", 'cyan'))
    print(color(f"║ [+] Total Hosts: {host[0]}                   ║", 'blue'))
    print(color(f"║ [+] Usable Hosts: {host[1]}                  ║", 'blue'))
    print(color(f"╚════════════════════════════════════════╝\n", 'yellow'))

if __name__ == '__main__':
    main()
