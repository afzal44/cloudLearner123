import boto3
import json

client = boto3.client('lambda')
ssm_client = boto3.client('ssm')

def lambda_handler(event, context):

    # -----------------------------------------------------------------------
    # Get the list of ARNs of cross-account IAM roles saved in SSM Parameter rolearnlist
    # -----------------------------------------------------------------------
    rolearnlist = []
    rolearnlist_from_ssm = ssm_client.get_parameter(Name='rolearnlist')
    rolearnlist_from_ssm_list = rolearnlist_from_ssm['Parameter']['Value'].split(",")
    rolearnlist = rolearnlist_from_ssm_list
    # -----------------------------------------------------------------------
    
    # -----------------------------------------------------------------------
    # Loop through the list of ARNs, asynchronously invoke invoke_slave lambda and pass ARN
    # -----------------------------------------------------------------------
    for rolearn in rolearnlist:
        x = {"ARN": rolearn}
        invoke_response = client.invoke(FunctionName="Invoke_slave",
                                        #  InvocationType='Event', #assync exec
                                         InvocationType='RequestResponse', #sync exec
                                         Payload=json.dumps(x))
        print(invoke_response)
