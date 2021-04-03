import time

def run_cmd(client, instance_id,cmd='uptime'):

    response = client.send_command(
        InstanceIds=[instance_id],
        DocumentName='SQLSERVERCMD',
        DocumentVersion="3"
        # Parameters={
        #     'commands': [
        #         # Simple test if a file exists
        #         # 'if [ -e /etc/hosts ]; then echo -n True; else echo -n False; fi'
        #         cmd
        #     ]
        # }
    )
    # print(":::GOT THIS RESPONSE==>:::",response)
    command_id = response['Command']['CommandId']
    tries = 0
    output = 'False'
    while tries < 10:
        tries = tries + 1
        try:
            time.sleep(0.5)  # some delay always required...
            result = client.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id,
            )
            if result['Status'] == 'InProgress':
                continue
            output = result['StandardOutputContent']
            break
        except client.exceptions.InvocationDoesNotExist:
            continue

    return str(output)