#!/usr/bin/python
'''
usage: ec2StopByTag.py - Called by Lambda function

Description: Stop all ec2 instances that have tag 'autooff'='True'. We should first create IAM Policy and execution role for Lambda function.

optional arguments:
  none

  https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/
  https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instance_status
'''

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Use filter method to retrieve all running EC2 instances tagged as AutoOff
    filters = [{
            'Name': 'tag:autooff',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    instances = ec2.instances.filter(Filters=filters)

    RunningInstances = [instance.id for instance in instances]
        
    if len(RunningInstances) > 0:
        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
        print (shuttingDown)

def main():
    lambda_handler(event, context)
          
if __name__ == "__main__":
    main()