#!/usr/bin/python
'''
usage: directConnectStatus.py [-h] -s <storagegatewayid>

Description: Monitors an AWS Storage Gateway included by parameter

optional arguments:
  -h, --help            show this help message and exit 
  -s <storagegatewayid>, --storagegateway <storagegatewayid>
                        StorageGateway ID to monitor

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.confirm_connection
'''

import argparse
import boto3

def get_parameters(args):

  client = boto3.client('directconnect') 
  response = client.describe_direct_connect_gateways(
    directConnectGatewayId=args.directconnect
  )
  for dxgw in response['directConnectGateways']:
    if dxgw['directConnectGatewayState'] == 'available':
      print("OK")
    else:
      print("KO")

def main():
  parser = argparse.ArgumentParser(description="Description: Monitors DX status")
  parser.add_argument('-d', '--directconnect', help="Direct Connect ID to monitor", required=True)
  args = parser.parse_args()

  get_parameters(args)

if __name__ == "__main__":
  main()