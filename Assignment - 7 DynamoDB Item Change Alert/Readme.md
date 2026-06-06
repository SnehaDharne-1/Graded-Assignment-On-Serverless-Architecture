# Assignment 7: DynamoDB Item Change Alert Using AWS Lambda, Boto3, and SNS

## Objective

The objective of this assignment is to automate notifications whenever an item in a DynamoDB table is modified. AWS Lambda will process DynamoDB Stream events and send detailed alerts through Amazon SNS whenever an item is updated.

This solution demonstrates event-driven serverless architecture using:

* Amazon DynamoDB
* DynamoDB Streams
* AWS Lambda
* Amazon SNS
* Boto3
* Amazon CloudWatch

---

# Architecture Overview

```text
DynamoDB Table
       │
       ▼
 DynamoDB Stream
       │
       ▼
   AWS Lambda
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

  * Amazon DynamoDB
  * AWS Lambda
  * Amazon SNS
  * AWS IAM
  * Amazon CloudWatch
* Basic understanding of AWS services and Python

---

# Step 1: Create DynamoDB Table

## Create Table

1. Navigate to **Amazon DynamoDB**.
2. Click **Create Table**.

### Configuration

| Setting       | Value        |
| ------------- | ------------ |
| Table Name    | EmployeeData |
| Partition Key | EmployeeID   |
| Key Type      | String       |

3. Leave other settings as default.
4. Click **Create Table**.

---

## Add Sample Items

After the table is created:

1. Open the table.
2. Navigate to:

```text
Explore Table Items
```

3. Click:

```text
Create Item
```

### Example Item 1

```json
{
  "EmployeeID": "101",
  "Name": "John",
  "Department": "IT",
  "Salary": "50000"
}
```

### Example Item 2

```json
{
  "EmployeeID": "102",
  "Name": "Alice",
  "Department": "HR",
  "Salary": "45000"
}
```

Save the items.

---

# Step 2: Create SNS Topic

## Create Topic

1. Navigate to **Amazon SNS**.
2. Click:

```text
Create Topic
```

3. Select:

```text
Standard Topic
```

### Configuration

| Setting      | Value                  |
| ------------ | ---------------------- |
| Topic Name   | DynamoDB-Change-Alerts |
| Display Name | DynamoDBAlerts         |

Click:

```text
Create Topic
```

---

## Create Email Subscription

1. Open the SNS Topic.
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

Verify the status becomes:

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

## Attach Policies

Attach the following policies:

```text
AWSLambdaBasicExecutionRole
```

```text
AmazonSNSFullAccess
```

```text
AmazonDynamoDBFullAccess
```

```text
AWSLambdaDynamoDBExecutionRole
```

> Note: For production environments, create a custom least-privilege policy instead of full access permissions.

---

## Role Name

```text
Lambda-DynamoDB-Alert-Role
```

Click:

```text
Create Role
```

---

# Step 4: Create Lambda Function

## Create Function

1. Navigate to **AWS Lambda**.
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

| Setting        | Value                      |
| -------------- | -------------------------- |
| Function Name  | DynamoDB-Change-Notifier   |
| Runtime        | Python 3.x                 |
| Architecture   | x86_64                     |
| Execution Role | Use Existing Role          |
| IAM Role       | Lambda-DynamoDB-Alert-Role |

Click:

```text
Create Function
```

---

# Step 5: Lambda Function Code

Replace the default Lambda code with the following:

```python
import json
import boto3

sns = boto3.client('sns')

SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"

def lambda_handler(event, context):

    for record in event['Records']:

        if record['eventName'] == 'MODIFY':

            old_image = record['dynamodb'].get('OldImage', {})
            new_image = record['dynamodb'].get('NewImage', {})

            message = (
                f"DynamoDB Item Updated\n\n"
                f"Old Value:\n{json.dumps(old_image, indent=2)}\n\n"
                f"New Value:\n{json.dumps(new_image, indent=2)}"
            )

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject='DynamoDB Item Change Alert',
                Message=message
            )

            print("SNS notification sent")

    return {
        'statusCode': 200,
        'body': 'Notification processed successfully'
    }
```

---

# Step 6: Update SNS Topic ARN

Replace:

```python
SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"
```

With your SNS Topic ARN:

```python
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:DynamoDB-Change-Alerts"
```

---

# Step 7: Deploy Lambda Function

Click:

```text
Deploy
```

Wait for successful deployment.

---

# Step 8: Enable DynamoDB Streams

1. Open your DynamoDB table.
2. Select:

```text
Exports and Streams
```

3. Under **DynamoDB Stream Details**:

```text
Enable Stream
```

### Stream View Type

Choose:

```text
New and Old Images
```

Click:

```text
Turn On Stream
```

---

# Step 9: Connect Stream to Lambda

1. Open:

```text
AWS Lambda → DynamoDB-Change-Notifier
```

2. Click:

```text
Add Trigger
```

3. Select:

```text
DynamoDB
```

4. Choose:

```text
EmployeeData Table Stream
```

5. Keep defaults.

6. Click:

```text
Add
```

---

# Step 10: Test the Solution

Navigate to:

```text
DynamoDB → EmployeeData
```

Open an existing item.

### Example Update

Before:

```json
{
  "EmployeeID": "101",
  "Name": "John",
  "Department": "IT",
  "Salary": "50000"
}
```

After:

```json
{
  "EmployeeID": "101",
  "Name": "John",
  "Department": "IT",
  "Salary": "60000"
}
```

Save the changes.

---

# Step 11: Verify SNS Alert

After a few seconds:

1. Check your email inbox.
2. You should receive an email notification.

### Example Alert

```text
Subject: DynamoDB Item Change Alert

DynamoDB Item Updated

Old Value:
{
  "Salary": {
    "S": "50000"
  }
}

New Value:
{
  "Salary": {
    "S": "60000"
  }
}
```

---

# Step 12: Verify CloudWatch Logs

Navigate to:

```text
CloudWatch → Log Groups
```

Open:

```text
/aws/lambda/DynamoDB-Change-Notifier
```

Example log output:

```text
START RequestId: abc123

SNS notification sent

END RequestId: abc123
```

---

# Expected Output

### Lambda Response

```json
{
  "statusCode": 200,
  "body": "Notification processed successfully"
}
```

### SNS Email Notification

```text
Subject: DynamoDB Item Change Alert

DynamoDB Item Updated

Old Value:
{ ... }

New Value:
{ ... }
```

---

# Screenshots Required for Submission

Include screenshots of:

### 1. DynamoDB Table

```text
EmployeeData Table
```

---

### 2. SNS Topic

```text
DynamoDB-Change-Alerts
```

---

### 3. SNS Email Alert

Screenshot showing received email notification.

---

### 4. Lambda Function

Screenshot of Lambda code and successful deployment.

---

### 5. CloudWatch Logs

Screenshot showing:

```text
SNS notification sent
```

---

### 6. DynamoDB Stream Configuration

Screenshot showing:

```text
Stream Enabled
View Type: New and Old Images
```

---

# Project Structure

```text
Assignment-7/
│
├── README.md
├── lambda_function.py
└── screenshots/
    ├── dynamodb-table.png
    ├── sns-topic.png
    ├── sns-email-alert.png
    ├── lambda-function.png
    ├── cloudwatch-logs.png
    └── dynamodb-stream.png
```

---

# Services Used

* Amazon DynamoDB
* DynamoDB Streams
* AWS Lambda
* Amazon SNS
* AWS IAM
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

# Workflow

```text
Update DynamoDB Item
          │
          ▼
 DynamoDB Stream Event
          │
          ▼
    AWS Lambda Triggered
          │
          ▼
 Extract Old and New Images
          │
          ▼
     Publish SNS Alert
          │
          ▼
      Email Notification
          │
          ▼
   CloudWatch Logging
```

---

# Learning Outcomes

After completing this assignment, you will be able to:

* Create and manage DynamoDB tables.
* Enable and configure DynamoDB Streams.
* Build event-driven serverless applications.
* Process DynamoDB Stream events using Lambda.
* Send notifications using Amazon SNS.
* Monitor Lambda execution with CloudWatch Logs.
* Implement real-time change tracking for database records.

---

# Best Practices

* Use least-privilege IAM permissions.
* Filter specific attributes before sending notifications.
* Store SNS Topic ARN in Lambda environment variables.
* Enable CloudWatch alarms for Lambda failures.
* Consider using Amazon EventBridge for advanced event routing.

---

# Author

**AWS Lambda, DynamoDB Streams, Boto3, and SNS – DynamoDB Item Change Alert Assignment**
