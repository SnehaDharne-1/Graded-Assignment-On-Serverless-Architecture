import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    try:

        instance_id = event['detail']['instance-id']

        current_date = datetime.utcnow().strftime(
            '%Y-%m-%d'
        )

        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {
                    'Key': 'LaunchDate',
                    'Value': current_date
                },
                {
                    'Key': 'Environment',
                    'Value': 'Dev'
                }
            ]
        )

        print(
            f"Successfully tagged {instance_id}"
        )

        return {
            'statusCode': 200
        }

    except Exception as e:

        print(str(e))

        return {
            'statusCode': 500
        }