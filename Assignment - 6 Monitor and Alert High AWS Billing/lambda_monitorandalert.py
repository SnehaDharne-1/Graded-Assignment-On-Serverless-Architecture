import datetime
import os
import boto3

# Define your configuration constants
# NOTE: Estimated charges are always stored in the us-east-1 (N. Virginia) region
REGION = "us-east-1"
THRESHOLD = 50.00  # Set your threshold in USD
# Paste your SNS Topic ARN here
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:BillingAlertTopic"


def lambda_handler(event, context):
    # 1. Initialize boto3 clients
    cloudwatch = boto3.client("cloudwatch", region_name=REGION)
    sns = boto3.client("sns", region_name=REGION)

    # Set up time window for the metric (CloudWatch billing metrics update every few hours)
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(days=1)

    try:
        # 2. Retrieve the AWS billing metric from CloudWatch
        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/Billing",
            MetricName="EstimatedCharges",
            Dimensions=[{"Name": "Currency", "Value": "USD"}],
            StartTime=start_time,
            EndTime=end_time,
            Period=86400,  # 24 hours in seconds
            Statistics=["Maximum"],
        )

        # Extract the billing amount
        datapoints = response.get("Datapoints", [])

        if not datapoints:
            print(
                "No billing data found. (Note: It can take up to 24 hours for fresh accounts to show metrics)."
            )
            return {"statusCode": 200, "body": "No data points found yet."}

        # Get the latest maximum cost
        current_billing = datapoints[0]["Maximum"]
        print(f"Current estimated billing: ${current_billing:.2f} USD")

        # 3 & 4. Compare with threshold and send SNS alert if exceeded
        if current_billing > THRESHOLD:
            alert_message = f"ALERT: Your AWS estimated billing has reached ${current_billing:.2f}, which exceeds your threshold of ${THRESHOLD:.2f}."
            print(f"Threshold exceeded! Sending SNS notification...")

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=alert_message,
                Subject="⚠️ AWS Billing Alert Threshold Exceeded!",
            )
        else:
            print("Billing is within safe limits. No alert sent.")

        return {
            "statusCode": 200,
            "body": f"Processed successfully. Current bill: ${current_billing:.2f}",
        }

    except Exception as e:
        print(f"Error encountered: {str(e)}")
        raise e