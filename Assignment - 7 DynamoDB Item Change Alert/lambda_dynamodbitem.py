import json
import boto3

# Initialize the SNS client
sns_client = boto3.client("sns")

# paste your actual SNS Topic ARN here
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:DynamoDB_Alert_Topic"


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Iterate through the batch of records sent by DynamoDB Streams
    for record in event["Records"]:
        event_name = record["eventName"]  # e.g., INSERT, MODIFY, REMOVE

        # We are specifically tracking updates (MODIFY), but this handles INSERT too
        if event_name in ["MODIFY", "INSERT"]:
            print(f"Processing {event_name} record...")

            # Extract data images
            new_image = record["dynamodb"].get("NewImage", {})
            old_image = record["dynamodb"].get("OldImage", {})

            # Format a clear, readable alert message
            alert_message = (
                f"🚨 DynamoDB Table Item Alert! 🚨\n\n"
                f"Operation Type: {event_name}\n"
                f"Table Source: {record['eventSourceARN'].split('/')[1]}\n\n"
                f"--- OLD ITEM STATE ---\n{json.dumps(old_image, indent=2)}\n\n"
                f"--- NEW ITEM STATE ---\n{json.dumps(new_image, indent=2)}\n"
            )

            # Publish the message to SNS
            try:
                response = sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=alert_message,
                    Subject=f"⚠️ DynamoDB Alert: Item {event_name}ed!",
                )
                print(
                    f"Successfully sent SNS notification. MessageId: {response['MessageId']}"
                )
            except Exception as e:
                print(f"Error sending SNS notification: {str(e)}")

    return {"statusCode": 200, "body": json.dumps("Successfully processed stream records.")}