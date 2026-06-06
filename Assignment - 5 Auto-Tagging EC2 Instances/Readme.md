# Assignment 5: Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3

## Objective

The objective of this assignment is to automate the tagging of newly launched EC2 instances using AWS Lambda and Boto3. Every new EC2 instance will automatically receive:

* The current launch date as a tag.
* A custom tag for resource identification and management.

This helps improve resource tracking, governance, auditing, and cost management.

---

# Architecture Overview

* **Amazon EC2**: Launches virtual machine instances.
* **Amazon EventBridge (CloudWatch Events)**: Detects EC2 launch events.
* **AWS Lambda**: Processes launch events and applies tags.
* **IAM Role**: Grants Lambda permission to tag EC2 instances.
* **Boto3**: AWS SDK for Python used within Lambda.

---

# Prerequisites

Before starting, ensure you have:

* An AWS Account
* Permissions to:

  * Launch EC2 Instances
  * Create Lambda Functions
  * Create IAM Roles
  * Create EventBridge Rules
* Basic understanding of AWS services and Python

---

# Step 1: Verify EC2 Access

1. Open the AWS Management Console.
2. Navigate to:

```text
EC2 Dashboard
```

3. Confirm that you can launch EC2 instances.

No EC2 instance needs to be created at this stage.

---

# Step 2: Create IAM Role for Lambda

## Create Role

1. Open **IAM Dashboard**.
2. Select:

```text
Roles → Create Role
```

3. Choose:

```text
Trusted Entity Type: AWS Service
Use Case: Lambda
```

4. Click **Next**.

---

## Attach Permissions

Attach the following policy:

```text
AmazonEC2FullAccess
```

> Note: This policy is used for educational purposes. In production environments, use least-privilege IAM policies.

---

## Role Name

```text
Lambda-EC2-AutoTag-Role
```

Click **Create Role**.

---

# Step 3: Create Lambda Function

## Create Function

1. Open **AWS Lambda**.
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

| Setting        | Value                   |
| -------------- | ----------------------- |
| Function Name  | EC2-Auto-Tagger         |
| Runtime        | Python 3.x              |
| Architecture   | x86_64                  |
| Execution Role | Use Existing Role       |
| IAM Role       | Lambda-EC2-AutoTag-Role |

Click **Create Function**.

---

# Step 4: Lambda Function Code

Replace the default Lambda code with the following:

```python
import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Retrieve Instance ID from EventBridge event
    instance_id = event['detail']['instance-id']

    # Current Date
    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    # Create Tags
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                'Key': 'LaunchDate',
                'Value': current_date
            },
            {
                'Key': 'Environment',
                'Value': 'Development'
            }
        ]
    )

    print(f"Successfully tagged instance: {instance_id}")

    return {
        'statusCode': 200,
        'instance_id': instance_id,
        'launch_date': current_date
    }
```

---

# Step 5: Deploy Lambda Function

1. Click:

```text
Deploy
```

2. Wait until deployment completes successfully.

---

# Step 6: Create EventBridge Rule

The EventBridge rule will automatically trigger Lambda whenever a new EC2 instance enters the running state.

---

## Open EventBridge

1. Navigate to:

```text
Amazon EventBridge
```

2. Click:

```text
Create Rule
```

---

## Rule Configuration

| Setting     | Value                               |
| ----------- | ----------------------------------- |
| Rule Name   | EC2-Auto-Tagging-Rule               |
| Description | Automatically tag new EC2 instances |
| Rule Type   | Rule with Event Pattern             |

---

## Event Source

Select:

```text
AWS Events or EventBridge Partner Events
```

---

## Event Pattern

Choose:

```text
Pre-defined Pattern by Service
```

### Service Provider

```text
AWS
```

### Service Name

```text
EC2
```

### Event Type

```text
EC2 Instance State-change Notification
```

### Specific State

```text
running
```

Example Event Pattern:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

---

## Configure Target

Select:

```text
Target Type: AWS Service
```

Choose:

```text
Lambda Function
```

Select:

```text
EC2-Auto-Tagger
```

Click:

```text
Create Rule
```

---

# Step 7: Launch a Test EC2 Instance

1. Navigate to:

```text
EC2 Dashboard
```

2. Click:

```text
Launch Instance
```

### Example Configuration

| Setting        | Value          |
| -------------- | -------------- |
| Name           | AutoTag-Test   |
| AMI            | Amazon Linux 2 |
| Instance Type  | t2.micro       |
| Key Pair       | Optional       |
| Security Group | Default        |

3. Click:

```text
Launch Instance
```

---

# Step 8: Verify Automatic Tagging

Wait approximately:

```text
30–60 Seconds
```

Navigate to:

```text
EC2 Dashboard → Instances
```

Select the newly launched instance.

Open:

```text
Tags Tab
```

Verify the following tags exist:

| Key         | Example Value |
| ----------- | ------------- |
| LaunchDate  | 2026-06-06    |
| Environment | Development   |

---

# Step 9: Verify CloudWatch Logs

Navigate to:

```text
CloudWatch → Log Groups
```

Open:

```text
/ aws / lambda / EC2-Auto-Tagger
```

You should see log entries similar to:

```text
Successfully tagged instance: i-0123456789abcdef0
```

---

# Expected Output

Example Lambda Response:

```json
{
  "statusCode": 200,
  "instance_id": "i-0123456789abcdef0",
  "launch_date": "2026-06-06"
}
```

---

# Project Structure

```text
Assignment-5/
│
├── README.md
└── lambda_function.py
```

---

# Services Used

* Amazon EC2
* AWS Lambda
* AWS IAM
* Amazon EventBridge
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

# Workflow

```text
Launch EC2 Instance
         │
         ▼
EC2 State Changes to Running
         │
         ▼
EventBridge Detects Event
         │
         ▼
Triggers Lambda Function
         │
         ▼
Lambda Retrieves Instance ID
         │
         ▼
Apply LaunchDate Tag
Apply Environment Tag
         │
         ▼
Store Logs in CloudWatch
```

---

# Learning Outcomes

After completing this assignment, you will be able to:

* Automate AWS resource tagging.
* Create event-driven architectures using EventBridge.
* Use Lambda functions to manage EC2 resources.
* Extract information from AWS event payloads.
* Apply tags programmatically using Boto3.
* Monitor Lambda execution using CloudWatch Logs.

---

# Best Practices

* Use consistent tag naming conventions.
* Create mandatory tagging policies using AWS Organizations.
* Restrict IAM permissions using least-privilege principles.
* Use EventBridge for serverless event-driven automation.
* Include additional tags such as:

  * Owner
  * Department
  * Project
  * CostCenter
  * Environment

---

# Author

**AWS Lambda & Boto3 – Auto-Tagging EC2 Instances on Launch Assignment**
