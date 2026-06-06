# Assignment 4: Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3

## Objective

The objective of this assignment is to automate the backup process of Amazon EBS volumes by creating snapshots and automatically deleting snapshots older than 30 days to optimize storage costs.

---

# Architecture Overview

* **Amazon EBS**: Provides block storage volumes for EC2 instances.
* **AWS Lambda**: Executes the snapshot creation and cleanup automation.
* **Amazon EventBridge (CloudWatch Events)**: Triggers Lambda on a schedule.
* **IAM Role**: Grants Lambda permission to manage EBS snapshots.
* **Boto3**: AWS SDK for Python used within Lambda.

---

# Prerequisites

Before starting, ensure you have:

* An AWS Account
* Access to:

  * Amazon EC2
  * Amazon EBS
  * AWS Lambda
  * AWS IAM
  * Amazon EventBridge (CloudWatch Events)
  * Amazon CloudWatch
* Basic knowledge of AWS services and Python

---

# Step 1: Create or Identify an EBS Volume

## Option 1: Use Existing EBS Volume

1. Navigate to **EC2 Dashboard**.
2. Select **Elastic Block Store → Volumes**.
3. Identify an existing EBS volume.
4. Note the:

```text
Volume ID (Example: vol-0123456789abcdef0)
```

---

## Option 2: Create a New EBS Volume

1. Open **EC2 Dashboard**.
2. Navigate to:

```text
Elastic Block Store → Volumes
```

3. Click **Create Volume**.

### Configuration

| Setting           | Value                |
| ----------------- | -------------------- |
| Volume Type       | gp3                  |
| Size              | 8 GiB                |
| Availability Zone | Same as EC2 Instance |

4. Click **Create Volume**.
5. Copy the generated Volume ID.

---

# Step 2: Create IAM Role for Lambda

## Create Role

1. Open **IAM Dashboard**.
2. Select **Roles → Create Role**.
3. Choose:

```text
Trusted Entity Type: AWS Service
Use Case: Lambda
```

4. Click **Next**.

---

## Attach Permissions

Attach:

```text
AmazonEC2FullAccess
```

> Note: This policy is used for educational purposes. In production environments, create a custom least-privilege policy.

---

## Role Name

```text
Lambda-EBS-Snapshot-Role
```

Click **Create Role**.

---

# Step 3: Create Lambda Function

## Create Function

1. Open **AWS Lambda**.
2. Click **Create Function**.
3. Select:

```text
Author from Scratch
```

---

## Configuration

| Setting        | Value                    |
| -------------- | ------------------------ |
| Function Name  | EBS-Snapshot-Manager     |
| Runtime        | Python 3.x               |
| Architecture   | x86_64                   |
| Execution Role | Use Existing Role        |
| IAM Role       | Lambda-EBS-Snapshot-Role |

Click **Create Function**.

---

# Step 4: Lambda Function Code

Replace the default Lambda code with the following:

```python
import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = 'vol-xxxxxxxxxxxxxxxxx'

def lambda_handler(event, context):

    # Create Snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated snapshot created by Lambda'
    )

    snapshot_id = snapshot['SnapshotId']

    print(f"Created Snapshot: {snapshot_id}")

    # Retention Period
    retention_date = datetime.now(timezone.utc) - timedelta(days=30)

    deleted_snapshots = []

    snapshots = ec2.describe_snapshots(
        OwnerIds=['self']
    )

    for snap in snapshots['Snapshots']:

        if snap['VolumeId'] == VOLUME_ID:

            start_time = snap['StartTime']

            if start_time < retention_date:

                ec2.delete_snapshot(
                    SnapshotId=snap['SnapshotId']
                )

                deleted_snapshots.append(snap['SnapshotId'])

                print(f"Deleted Snapshot: {snap['SnapshotId']}")

    return {
        'statusCode': 200,
        'created_snapshot': snapshot_id,
        'deleted_snapshots': deleted_snapshots
    }
```

---

# Step 5: Update Volume ID

Replace:

```python
VOLUME_ID = 'vol-xxxxxxxxxxxxxxxxx'
```

With your actual EBS Volume ID:

```python
VOLUME_ID = 'vol-0123456789abcdef0'
```

---

# Step 6: Deploy Lambda Function

1. Click **Deploy**.
2. Wait for deployment to complete successfully.

---

# Step 7: Create Test Event

1. Click **Test**.
2. Configure:

```text
Event Name: SnapshotTest
```

3. Use default payload:

```json
{}
```

4. Save.

---

# Step 8: Invoke Lambda Function

Click:

```text
Test
```

The Lambda function will:

1. Create a new snapshot.
2. Retrieve all snapshots owned by your account.
3. Identify snapshots older than 30 days.
4. Delete old snapshots.
5. Log all actions in CloudWatch.

---

# Step 9: Verify Snapshot Creation

Navigate to:

```text
EC2 Dashboard → Elastic Block Store → Snapshots
```

Verify:

* New snapshot is created.
* Status changes from:

```text
Pending → Completed
```

---

# Step 10: Verify Snapshot Cleanup

Under the Snapshots page:

* Snapshots older than 30 days should no longer appear.
* Recent snapshots should remain available.

---

# Bonus: Schedule Automatic Backups

Instead of manually invoking Lambda, configure EventBridge.

---

## Create EventBridge Rule

1. Open **Amazon EventBridge**.
2. Click **Create Rule**.

### Rule Configuration

| Setting   | Value             |
| --------- | ----------------- |
| Rule Name | Weekly-EBS-Backup |
| Rule Type | Schedule          |

---

### Schedule Pattern

Example: Run every Sunday at midnight UTC

```text
cron(0 0 ? * SUN *)
```

Or every 7 days:

```text
rate(7 days)
```

---

### Target

Select:

```text
AWS Lambda Function
```

Choose:

```text
EBS-Snapshot-Manager
```

Click **Create Rule**.

---

# Step 11: Verify Scheduled Execution

After the scheduled time:

1. Open CloudWatch Logs.
2. Navigate to:

```text
/aws/lambda/EBS-Snapshot-Manager
```

Verify logs similar to:

```text
Created Snapshot: snap-0abc123def456ghi7
Deleted Snapshot: snap-0xyz987uvw654rst3
```

---

# Expected Output

Example Lambda Response:

```json
{
  "statusCode": 200,
  "created_snapshot": "snap-0abc123def456ghi7",
  "deleted_snapshots": [
    "snap-0xyz987uvw654rst3",
    "snap-0qwe456asd789zxc1"
  ]
}
```

---

# Project Structure

```text
Assignment-4/
│
├── README.md
└── lambda_function.py
```

---

# Services Used

* Amazon EC2
* Amazon EBS
* AWS Lambda
* AWS IAM
* Amazon EventBridge
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

# Workflow

```text
EventBridge Schedule
          │
          ▼
    AWS Lambda
          │
          ▼
Create EBS Snapshot
          │
          ▼
List Existing Snapshots
          │
          ▼
Identify Snapshots Older Than 30 Days
          │
          ▼
Delete Old Snapshots
          │
          ▼
Store Logs in CloudWatch
```

---

# Learning Outcomes

After completing this assignment, you will be able to:

* Create and manage EBS volumes.
* Automate EBS snapshot backups.
* Delete old snapshots based on retention policies.
* Configure Lambda functions using Python.
* Use Boto3 to manage EC2 resources.
* Schedule automated tasks using EventBridge.
* Monitor AWS services using CloudWatch logs.

---

# Best Practices

* Use custom IAM policies with minimum required permissions.
* Tag snapshots for easier management.
* Enable monitoring through CloudWatch Alarms.
* Test automation in a non-production environment.
* Regularly review backup retention policies to optimize costs.

---

# Author

**AWS Lambda & Boto3 – Automatic EBS Snapshot and Cleanup Assignment**
