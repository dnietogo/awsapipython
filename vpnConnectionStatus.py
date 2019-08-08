#!/usr/bin/python
'''
usage: vpnConnectionStatus.py [-h] -v <vpnid>

Description: Monitors an AWS VPN Connection status included by parameter

optional arguments:
  -h, --help            show this help message and exit
  -v <vpnconnectionid>, --vpnconnectionid <vpnconnectionid>
                        VPN Connection ID to monitor

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpn_connections
'''

import argparse
import boto3

def get_parameters(args):

  client = boto3.client('ec2')
  response = client.describe_vpn_connections(
    VpnConnectionIds=args.vpnconnectionid
  )
  
  for vpncon in response['VpnConnections']:
    if vpncon['State'] == 'available':
      print("OK")
    else:
      print("KO")

def main():
  parser = argparse.ArgumentParser(description="Description: Monitors Site-to-Site VPN Connection status")
  parser.add_argument('-v', '--vpnconnectionid', help="VPN Connection ID to monitor", required=True)
  args = parser.parse_args()

  get_parameters(args)

if __name__ == "__main__":
  main()