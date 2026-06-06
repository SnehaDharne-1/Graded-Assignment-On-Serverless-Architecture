# Assignment 1: Automated Instance Management Using AWS Lambda and Boto3

## Objective

The objective of this assignment is to automate the management of Amazon EC2 instances using AWS Lambda and Boto3. The Lambda function will automatically start or stop EC2 instances based on specific tags assigned to them.

---

## Architecture Overview

* **Amazon EC2**: Hosts the instances to be managed.
* **AWS Lambda**: Executes the automation logic.
* **IAM Role**: Grants Lambda permission to manage EC2 instances.
* **Boto3**: AWS SDK for Python used within Lambda to interact with EC2.

---

## Prerequisites

Before starting, ensure you have:

* An AWS Account
* Basic knowledge of AWS services
* Access to:

  * Amazon EC2
  * AWS Lambda
  * AWS IAM

---

## Step 1: Create EC2 Instances

### Instance 1 (Auto-Stop)

1. Navigate to **EC2 Dashboard**.
2. Click **Launch Instance**.
3. Configure:

   * Name: `AutoStop-Instance`
   * AMI: Amazon Linux 2
   * Instance Type: `t2.micro`
4. Under **Tags**, add:

| Key    | Value     |
| ------ | --------- |
| Action | Auto-Stop |

5. Launch the instance.

---

### Instance 2 (Auto-Start)

1. Launch another EC2 instance.
2. Configure:

   * Name: `AutoStart-Instance`
   * AMI: Amazon Linux 2
   * Instance Type: `t2.micro`
3. Under **Tags**, add:

| Key    | Value      |
| ------ | ---------- |
| Action | Auto-Start |

4. Launch the instance.

---

## Step 2: Create IAM Role for Lambda

### Create Role

1. Navigate to **IAM Dashboard**.
2. Select **Roles** → **Create Role**.
3. Choose:

   * Trusted Entity: **AWS Service**
   * Use Case: **Lambda**
4. Click **Next**.

### Attach Permissions

Search and attach:

```
AmazonEC2FullAccess
```

> Note: This policy is used for learning purposes. In production environments, follow the principle of least privilege.

### Role Name

```
Lambda-EC2-Management-Role
```

Click **Create Role**.

---

## Step 3: Create Lambda Function

### Create Function

1. Navigate to **AWS Lambda**.
2. Click **Create Function**.
3. Select:

```
Author from scratch
```

### Configuration

| Setting        | Value                      |
| -------------- | -------------------------- |
| Function Name  | EC2-Auto-Management        |
| Runtime        | Python 3.x                 |
| Architecture   | x86_64                     |
| Execution Role | Use existing role          |
| IAM Role       | Lambda-EC2-Management-Role |

Click **Create Function**.

---

## Step 4: Lambda Function Code

Replace the default Lambda code with the following:

```python
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Find instances tagged Auto-Stop
    auto_stop_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Stop']
            }
        ]
    )

    stop_ids = []

    for reservation in auto_stop_instances['Reservations']:
        for instance in reservation['Instances']:
            stop_ids.append(instance['InstanceId'])

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Stopped Instances: {stop_ids}")

    # Find instances tagged Auto-Start
    auto_start_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start']
            }
        ]
    )

    start_ids = []

    for reservation in auto_start_instances['Reservations']:
        for instance in reservation['Instances']:
            start_ids.append(instance['InstanceId'])

    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Started Instances: {start_ids}")

    return {
        'statusCode': 200,
        'body': 'EC2 instance management completed successfully.'
    }
```

---

## Step 5: Deploy the Lambda Function

1. Click **Deploy**.
2. Wait for the deployment to complete successfully.

---

## Step 6: Test the Lambda Function

### Create Test Event

1. Click **Test**.
2. Configure:

```
Event Name: TestEvent
```

3. Leave the JSON payload as:

```json
{}
```

4. Save.

---

### Invoke Function

Click:

```
Test
```

The Lambda function will:

* Stop all EC2 instances tagged:

  ```
  Action = Auto-Stop
  ```

* Start all EC2 instances tagged:

  ```
  Action = Auto-Start
  ```

---

## Step 7: Verify Results

Navigate to:

```
EC2 Dashboard → Instances
```

Verify:

| Instance Tag | Expected State |
| ------------ | -------------- |
| Auto-Stop    | Stopped        |
| Auto-Start   | Running        |

---

## CloudWatch Logs Verification

1. Open **CloudWatch**.
2. Navigate to:

```
Log Groups
```

3. Open the Lambda log group:

```
/aws/lambda/EC2-Auto-Management
```

You should see logs similar to:

```text
Stopped Instances: ['i-0123456789abcdef0']
Started Instances: ['i-0fedcba9876543210']
```

---

## Expected Output

Example Lambda Response:

```json
{
  "statusCode": 200,
  "body": "EC2 instance management completed successfully."
}
```

---

## Project Structure

```text
Assignment-1/
│
├── README.md
└── lambda_function.py
```

---

## Services Used

* AWS EC2
* AWS Lambda
* AWS IAM
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

## Learning Outcomes

After completing this assignment, you will be able to:

* Create and configure EC2 instances.
* Apply tags to AWS resources.
* Create IAM roles and attach permissions.
* Develop AWS Lambda functions using Python.
* Use Boto3 to manage EC2 instances.
* Monitor Lambda execution through CloudWatch logs.
* Automate AWS infrastructure operations.

---

## Author

**AWS Lambda & Boto3 EC2 Automation Assignment**
