#!/usr/bin/python

""" 
Description: Retrieves information about all IAM users, groups, roles, and policies in your AWS account, including their relationships to one another.
    If it's going to be deployed in a server without "aws configure" we can include aws_access_key_id and aws_secret_access_key as parameters.
    Link to docu: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_account_authorization_details 
"""
import argparse
import boto3
import json
from bson import json_util

def get_parameters(args):
    # Get access key id and secret access key from console and send as parameters
    client = boto3.client(
        'iam',
        aws_access_key_id = args.accessKey,
        aws_secret_access_key = args.secretAccessKey
    )

    # Filtering results by User, to get all users we have created, and custom managed policies. We can quit Filter to retrieve all data
    response = client.get_account_authorization_details(
        Filter = ['User','LocalManagedPolicy']
    )

    ## Filtering results in order to get only "UserName" and "AttachedManagedPolicies.PolicyName" -NO FUNCIONA, ni se recupera, ni se escribe en el fichero
    # user_list = response['UserDetailList']  
    # for user in user_list:
    #     print(user['UserName'])
        
    #     mPolicies_list = user_list['AttachedManagedPolicies']
    #     for mpolicy in mPolicies_list:
    #         print(mpolicy['PolicyName'])

    ## Filtering results in order to get only "PolicyName" and "PolicyVersionList.Document" (there are some versions for every PolicyName and we want to get only max VersionId)
    # managed_policies_list = response['Policies'] -NO FUNCIONA, ni se recupera, ni se escribe en el fichero
    # for policy in managed_policies_list:
    #     print(policy['PolicyName'])
    #     print(policy['PolicyVersionList'])

    # Write the result in a file 
    with open('AccountAuthorizationDetails.json','w') as outfile:
        json.dump(response, outfile, default=json_util.default)

def main():
    parser = argparse.ArgumentParser(description="Retrieves information about all IAM users, groups, roles, and policies in your AWS account, including their relationships to one another.")
    parser.add_argument('-a', '--accessKey', help="Specify Access Key ID", required=False)
    parser.add_argument('-s', '--secretAccessKey', help="Specify Secret Access Key ID", required=False)
    args = parser.parse_args()
    get_parameters(args)

if __name__ == "__main__":
    main()   