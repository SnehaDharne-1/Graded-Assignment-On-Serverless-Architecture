# Assignment 6: Monitor and Alert High AWS Billing Using AWS Lambda, Boto3, and SNS

## Objective

The objective of this assignment is to create an automated billing monitoring solution that checks AWS account charges daily and sends an alert notification when the billing amount exceeds a predefined threshold.

This solution uses:

* AWS Lambda
* Amazon CloudWatch Billing Metrics
* Amazon SNS (Simple Notification Service)
* Amazon EventBridge (CloudWatch Events)
* Boto3

---

# Architecture Overview

```text
AWS Billing Metrics
         │
         ▼
   CloudWatch
         │
         ▼
   AWS Lambda
         │
         ▼
 Compare Billing Threshold
         │
         ▼
    Amazon SNS
         │
         ▼
   Email Alert
```

---

# Prerequisites

Before starting, ensure you have:

* An AWS Account
* Access to:

  * AWS Lambda
  * Amazon SNS
  * Amazon CloudWatch
  * Amazon EventBridge
  * AWS IAM
* Billing Alerts Enabled in AWS

---

# Step 1: Enable AWS Billing Metrics

AWS Billing Metrics are disabled by default.

### Enable Billing Alerts

1. Log in as the AWS Account Root User.
2. Navigate to:

```text
AWS Billing Console
```

3. Click:

```text
Billing Preferences
```

4. Enable:

```text
Receive Billing Alerts
```

5. Save changes.

> Note: Billing metrics may take several hours to appear in CloudWatch after enabling.

---

# Step 2: Create SNS Topic

## Create Topic

1. Navigate to:

```text
Amazon SNS
```

2. Click:

```text
Create Topic
```

3. Select:

```text
Standard Topic
```

### Configuration

| Setting      | Value              |
| ------------ | ------------------ |
| Topic Name   | AWS-Billing-Alerts |
| Display Name | BillingAlerts      |

Click:

```text
Create Topic
```

---

## Create Email Subscription

1. Open the created topic.
2. Click:

```text
Create Subscription
```

### Configuration

| Setting  | Value                                                   |
| -------- | ------------------------------------------------------- |
| Protocol | Email                                                   |
| Endpoint | [your-email@example.com](mailto:your-email@example.com) |

Click:

```text
Create Subscription
```

---

## Confirm Subscription

1. Check your email inbox.
2. Open the SNS confirmation email.
3. Click:

```text
Confirm Subscription
```

Status should change to:

```text
Confirmed
```

---

# Step 3: Create IAM Role for Lambda

## Create Role

1. Navigate to:

```text
IAM → Roles → Create Role
```

2. Choose:

```text
AWS Service → Lambda
```

3. Click **Next**.

---

## Attach Permissions

Attach the following AWS managed policies:

```text
CloudWatchReadOnlyAccess
```

```text
AmazonSNSFullAccess
```

```text
AWSLambdaBasicExecutionRole
```

> Note: In production, create a custom least-privilege policy instead of using full access.

---

## Role Name

```text
Lambda-Billing-Monitor-Role
```

Click:

```text
Create Role
```

---

# Step 4: Create Lambda Function

## Create Function

1. Navigate to:

```text
AWS Lambda
```

2. Click:

```text
Create Function
```

3. Choose:

```text
Author From Scratch
```

---

## Configuration

| Setting        | Value                       |
| -------------- | --------------------------- |
| Function Name  | AWS-Billing-Monitor         |
| Runtime        | Python 3.x                  |
| Architecture   | x86_64                      |
| Execution Role | Use Existing Role           |
| IAM Role       | Lambda-Billing-Monitor-Role |

Click:

```text
Create Function
```

---

# Step 5: Lambda Function Code

Replace the default code with the following:

```python
import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

THRESHOLD = 50.0

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:AWS-Billing-Alerts"

def lambda_handler(event, context):

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/Billing',
        MetricName='EstimatedCharges',
        Dimensions=[
            {
                'Name': 'Currency',
                'Value': 'USD'
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=['Maximum']
    )

    datapoints = response['Datapoints']

    if not datapoints:
        print("No billing data available.")
        return

    current_bill = max(
        point['Maximum']
        for point in datapoints
    )

    print(f"Current AWS Bill: ${current_bill}")

    if current_bill > THRESHOLD:

        message = (
            f"AWS Billing Alert!\n\n"
            f"Current Charges: ${current_bill}\n"
            f"Threshold: ${THRESHOLD}"
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='AWS Billing Alert',
            Message=message
        )

        print("SNS Alert Sent")

    else:
        print("Billing within threshold")

    return {
        "statusCode": 200,
        "current_bill": current_bill
    }
```

---

# Step 6: Update Configuration Values

Replace:

```python
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:AWS-Billing-Alerts"
```

with your SNS Topic ARN.

Example:

```python
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:987654321098:AWS-Billing-Alerts"
```

---

### Optional: Change Billing Threshold

Default threshold:

```python
THRESHOLD = 50.0
```

Example:

```python
THRESHOLD = 10.0
```

This triggers alerts when charges exceed $10.

---

# Step 7: Deploy Lambda Function

Click:

```text
Deploy
```

Wait until deployment succeeds.

---

# Step 8: Create Test Event

1. Click:

```text
Test
```

2. Configure:

```text
Event Name: BillingTest
```

3. Use default payload:

```json
{}
```

4. Save.

---

# Step 9: Manually Invoke Lambda

Click:

```text
Test
```

The Lambda function will:

1. Retrieve current AWS billing charges.
2. Compare against the threshold.
3. Send an SNS email alert if exceeded.
4. Log execution details in CloudWatch.

---

# Step 10: Configure Daily Automation (Bonus)

Instead of running manually, schedule Lambda daily using EventBridge.

---

## Create EventBridge Rule

1. Open:

```text
Amazon EventBridge
```

2. Click:

```text
Create Rule
```

---

### Configuration

| Setting   | Value                 |
| --------- | --------------------- |
| Rule Name | Daily-Billing-Monitor |
| Rule Type | Schedule              |

---

### Schedule Expression

Run once per day:

```text
rate(1 day)
```

Or every day at midnight UTC:

```text
cron(0 0 * * ? *)
```

---

### Select Target

Choose:

```text
AWS Lambda Function
```

Target:

```text
AWS-Billing-Monitor
```

Click:

```text
Create Rule
```

---

# Step 11: Verify Email Alerts

If billing exceeds the configured threshold:

1. Check your email inbox.
2. You should receive a message similar to:

```text
Subject: AWS Billing Alert

AWS Billing Alert!

Current Charges: $65.42
Threshold: $50.00
```

---

# Step 12: Verify CloudWatch Logs

Navigate to:

```text
CloudWatch → Log Groups
```

Open:

```text
/aws/lambda/AWS-Billing-Monitor
```

Example logs:

```text
Current AWS Bill: $65.42
SNS Alert Sent
```

or

```text
Current AWS Bill: $12.75
Billing within threshold
```

---

# Expected Output

Example Lambda Response

```json
{
  "statusCode": 200,
  "current_bill": 65.42
}
```

---

# Project Structure

```text
Assignment-6/
│
├── README.md
└── lambda_function.py
```

---

# Services Used

* AWS Lambda
* Amazon SNS
* Amazon CloudWatch
* Amazon EventBridge
* AWS IAM
* Boto3 (AWS SDK for Python)

---

# Workflow

```text
CloudWatch Billing Metrics
            │
            ▼
       AWS Lambda
            │
            ▼
  Compare Billing Amount
            │
     ┌──────┴──────┐
     │             │
     ▼             ▼
Below Limit   Above Limit
     │             │
     ▼             ▼
 No Action     SNS Alert
                   │
                   ▼
              Email Sent
```

---

# Learning Outcomes

After completing this assignment, you will be able to:

* Enable AWS Billing Metrics.
* Monitor AWS account charges programmatically.
* Retrieve CloudWatch billing metrics using Boto3.
* Send notifications using Amazon SNS.
* Automate monitoring using EventBridge.
* Implement cost-monitoring automation in AWS.
* Use CloudWatch Logs for troubleshooting.

---

# Best Practices

* Use custom IAM policies with minimum required permissions.
* Configure multiple notification recipients.
* Monitor costs daily or hourly.
* Set multiple billing thresholds (Warning, Critical).
* Integrate SNS with Slack, Teams, or PagerDuty for enterprise alerting.
* Consider AWS Budgets for advanced cost management.

---

# Author

**AWS Lambda, Boto3, and SNS – Monitor and Alert High AWS Billing Assignment**
