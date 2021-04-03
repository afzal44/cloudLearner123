import json
import boto3
from command1 import run_cmd
s3 = boto3.resource('s3')
client = boto3.client('ssm')
time_limit = 1

def lambda_handler(event, context):
    filters = [
{
'Name': 'instance-state-name',
'Values': ['running']
}
]
    # instances = ec2.instances.filter(Filters = filters)
    ssm_instances = [i['InstanceId'] for i in client.describe_instance_information()['InstanceInformationList'] if i['PingStatus'] == 'Online'] # must be online instance list
    print(ssm_instances)

    RunningInstances = []
    instanceList = []

    for instance_id in ssm_instances:
        RunningInstances.append(instance_id)
        result = run_cmd(client,instance_id)
        # print(type(result))
        print(":::::::Result from command::::",result)
        # if time_limit<int(result.split(" ")[3]):
        #     instanceList.append({'InstanceId':instance_id,'cmd_res':run_cmd(client,instance_id,cmd='sudo yum list installed').strip().split('\n')})
            

    # s3.Object(
    #             'cloudlearnerwork',
    #                 'instanceList.txt').put(Body = str(instanceList))
    if len(instanceList) == 0:
        instanceList = f"No Instance running for {time_limit} minutes"
    return {
   "statusCode": 200,
   "body": instanceList
    }