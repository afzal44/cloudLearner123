import boto3
import datetime
import time
from command import run_cmd

stsclient = boto3.client('sts')
s3client = boto3.resource('s3')


def lambda_handler(event, context):

    # -----------------------------------------------------------------------
    # initiating a session using ARN of the IAM role
    # -----------------------------------------------------------------------
    rolearn = event['ARN']
    awsaccount = stsclient.assume_role(
        RoleArn=rolearn,
        RoleSessionName='awsaccount_session'
    )
    ACCESS_KEY = awsaccount['Credentials']['AccessKeyId']
    SECRET_KEY = awsaccount['Credentials']['SecretAccessKey']
    SESSION_TOKEN = awsaccount['Credentials']['SessionToken']

    # -----------------------------------------------------------------------
    # create a list of all currently available aws regions
    # -----------------------------------------------------------------------
    # ec2 = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_session_token=SESSION_TOKEN)
    ssmclient = boto3.client('ssm',aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_session_token=SESSION_TOKEN,region_name='eu-west-1')
    ssm_instances = [i['InstanceId'] for i in ssmclient.describe_instance_information()['InstanceInformationList'] if i['PingStatus'] == 'Online'] # must be online instance list
    print(ssm_instances)
    try:
        result = ''
        for instance_id in ssm_instances:
            # RunningInstances.append(instance_id)
            result = run_cmd(ssmclient,instance_id)
            print(result)
    except Exception as e:
        result = e
    
    # -----------------------------------------------------------------------
    start = '::'
    end = ':'
    awsaccountid = rolearn[rolearn.find(start)+len(start):rolearn.rfind(end)] # getting awsaccount ID from IAM Role ARN
    domain = 'cloudlearnerwork1'  # S3 bucket name where HTML page will be saved (must be changed)
    htmlfilename = f'awsaccount-{awsaccountid}-SSm-Out.text'  # making unique name for HTML file
    s3client.Object(domain, htmlfilename).put(Body=result, ContentType='text/html')
    return result
