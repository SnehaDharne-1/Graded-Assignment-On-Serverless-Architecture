import boto3

# Initialize EC2 client
ec2 = boto3.client('ec2', region_name='ap-south-1')

def lambda_handler(event, context):

    # -----------------------------
    # Find instances with Auto-Stop
    # -----------------------------
    stop_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Stop']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    stop_instances = []

    for reservation in stop_response['Reservations']:
        for instance in reservation['Instances']:
            stop_instances.append(instance['InstanceId'])

    # Stop instances
    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print("Stopped Instances:", stop_instances)
    else:
        print("No instances found for Auto-Stop")


    # -----------------------------
    # Find instances with Auto-Start
    # -----------------------------
    start_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['stopped']
            }
        ]
    )

    start_instances = []

    for reservation in start_response['Reservations']:
        for instance in reservation['Instances']:
            start_instances.append(instance['InstanceId'])

    # Start instances
    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print("Started Instances:", start_instances)
    else:
        print("No instances found for Auto-Start")


    return {
        'statusCode': 200,
        'body': 'EC2 instances managed successfully'
    }