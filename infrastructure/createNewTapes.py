#!/usr/bin/python

""" 
Description: Creates virtual tapes. We have two options: 1) Deploy a defined number of tapes in all VTL SGW (without -g option) 2) Deploy a defined number of tapes in a VTL SGW (with -g option)
    Link to docu: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client.create_tapes 
"""
import argparse
import boto3
import random


def get_parameters(args):
    barPrefix = args.barprefix
    numTapes = args.numtapes
    hash = random.getrandbits(256)
    token = ("%064x" % hash)
    tag_client = args.tagclient

    if args.tagsubclient is None:  # If tag_subclient is not included, create it in blank
        tag_subclient = ''
    else:
        tag_subclient = args.tagsubclient

    storagegateways = {
        'sgw1': 'arn:aws:storagegateway:XXX',
        'sgw2': 'arn:aws:storagegateway:XXX'
    }

    gateways = []

    pool = "DEEP_ARCHIVE"
    tapeSize = 2199023255552  # 2TB in bytes, max 2,5TB

    tags = [
        {
            'Key': 'owner',
            'Value': 'OWNER'
        },
        {
            'Key': 'client',
            'Value': tag_client
        },
        {
            'Key': 'subclient',
            'Value': tag_subclient
        }
    ]  # Tags to send via REST API

    client = boto3.client('storagegateway')

    if args.storagegateway is not None:
        response = client.create_tapes(GatewayARN=storagegateways[args.storagegateway], TapeSizeInBytes=tapeSize, ClientToken=token,
                                       NumTapesToCreate=numTapes, TapeBarcodePrefix=barPrefix, KMSEncrypted=False, PoolId=pool, Tags=tags)
        print(response)

    else:
        response = client.list_gateways()
        for gws in response['Gateways']:  # Sift only VLT SGW
            if gws['GatewayType'] == 'VTL' and gws['GatewayOperationalState'] == 'ACTIVE':
                gateways.append(gws['GatewayARN'])

        for gateway in gateways:  # Create new tapes
            response = client.create_tapes(GatewayARN=gateway, TapeSizeInBytes=tapeSize, ClientToken=token,
                                           NumTapesToCreate=numTapes, TapeBarcodePrefix=barPrefix, KMSEncrypted=False, PoolId=pool, Tags=tags)
            print(response)


def main():
    parser = argparse.ArgumentParser(
        description="Description: creates virtual tapes on each existing VTGW")
    parser.add_argument('-p', '--barprefix', help="prefix for barcode", choices=[
                        'BAR1', 'BAR2', 'BAR3'], required=True, metavar='<barcodeprefix>')
    parser.add_argument('-n', '--numtapes', help="number of tapes to create, range between 1 and 20",
                        type=int, choices=range(1, 11), required=True, metavar='[1-11]')
    parser.add_argument('-c', '--tagclient', help="backup client to include", choices=[
                        'TagClient1', 'TagClient2', 'TagClient3'], required=True, metavar='<tagclient>')
    parser.add_argument('-g', '--storagegateway', help="storage gateway where deploy tapes",
                        choices=['sgw1', 'sgw2'], required=False, metavar='<storagegateway>')
    args = parser.parse_args()

    if (args.tagclient == 'RACPROD' or args.tagclient == 'Accounting' or args.tagclient == 'Invoicing') and args.tagsubclient is None:
        parser.error('When --tagclient is ' + args.tagclient +
                     ', subclient parameter is mandatory')
    get_parameters(args)


if __name__ == "__main__":
    main()
