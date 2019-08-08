#!/usr/bin/python
'''
usage: storageGatewaysStatus.py [-h] -s <storagegatewayid>

Description: Monitors an AWS Storage Gateway included by parameter

optional arguments:
  -h, --help            show this help message and exit
  -s <storagegatewayid>, --storagegateway <storagegatewayid>
                        StorageGateway ID to monitor

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.describe_gateway_information
'''

import argparse
import boto3

def get_parameters(args):

  client = boto3.client('storagegateway')
  response = client.describe_gateway_information(
    GatewayARN=args.storagegateway
  )
  if response['GatewayState'] == 'RUNNING':
    print("OK")
  else:
    print("KO")

def main():
  parser = argparse.ArgumentParser(description="Description: Monitors SGW status")
  parser.add_argument('-s', '--storagegateway', help="StorageGateway ID to monitor", required=True)
  args = parser.parse_args()

  get_parameters(args)

if __name__ == "__main__":
  main()