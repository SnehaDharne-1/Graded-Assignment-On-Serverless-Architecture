# Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## Objective

The objective of this assignment is to automate the cleanup of old files stored in an Amazon S3 bucket using AWS Lambda and Boto3. The Lambda function will identify and delete files that are older than 30 days.

---

# Architecture Overview

* **Amazon S3**: Stores files and objects.
* **AWS Lambda**: Executes the cleanup logic.
* **IAM Role**: Provides permissions to access and delete S3 objects.
* **Boto3**: AWS SDK for Python used within Lambda.

---

# Prerequisites

Before starting, ensure you have:

* An AWS Account
* Access to:

  * Amazon S3
  * AWS Lambda
  * AWS IAM
  * Amazon CloudWatch
* Basic knowledge of Python and AWS services

---

# Step 1: Create an S3 Bucket

## Create Bucket

1. Navigate to the AWS Management Console.
2. Open **Amazon S3**.
3. Click **Create Bucket**.

### Configuration

| Setting             | Value                    |
| ------------------- | ------------------------ |
| Bucket Name         | unique-s3-cleanup-bucket |
| AWS Region          | Any preferred region     |
| Object Ownership    | ACLs Disabled            |
| Block Public Access | Enabled                  |

4. Click **Create Bucket**.

---

## Upload Test Files

1. Open the newly created bucket.
2. Click **Upload**.
3. Upload multiple files.

Example:

```text
file1.txt
file2.pdf
file3.jpg
file4.docx
```

4. Ensure some files have a Last Modified date older than 30 days.

> Note: For testing purposes, you may use older files or simulate older timestamps through controlled testing methods.

---

# Step 2: Create IAM Role for Lambda

## Create Role

1. Open **IAM Dashboard**.
2. Select **Roles** → **Create Role**.
3. Choose:

```text
Trusted Entity Type: AWS Service
Use Case: Lambda
```

4. Click **Next**.

---

## Attach Permissions

Search and attach:

```text
AmazonS3FullAccess
```

> Note: This policy is used for educational purposes. In production environments, use a custom least-privilege policy.

---

## Role Name

```text
Lambda-S3-Cleanup-Role
```

Click **Create Role**.

---

# Step 3: Create Lambda Function

## Create Function

1. Open **AWS Lambda**.
2. Click **Create Function**.
3. Choose:

```text
Author from Scratch
```

---

## Configuration

| Setting        | Value                  |
| -------------- | ---------------------- |
| Function Name  | S3-Bucket-Cleanup      |
| Runtime        | Python 3.x             |
| Architecture   | x86_64                 |
| Execution Role | Use Existing Role      |
| IAM Role       | Lambda-S3-Cleanup-Role |

Click **Create Function**.

---

# Step 4: Lambda Function Code

Replace the default Lambda code with the following:

```python
import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'your-bucket-name'

def lambda_handler(event, context):

    deleted_files = []

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("Bucket is empty.")
        return

    threshold_date = datetime.now(timezone.utc) - timedelta(days=30)

    for obj in response['Contents']:

        if obj['LastModified'] < threshold_date:

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=obj['Key']
            )

            deleted_files.append(obj['Key'])
            print(f"Deleted: {obj['Key']}")

    return {
        'statusCode': 200,
        'deleted_files': deleted_files
    }
```

---

# Step 5: Update Bucket Name

Replace:

```python
BUCKET_NAME = 'your-bucket-name'
```

With your actual bucket name:

```python
BUCKET_NAME = 'my-s3-cleanup-bucket'
```

---

# Step 6: Deploy Lambda Function

1. Click **Deploy**.
2. Wait until deployment completes successfully.

---

# Step 7: Create Test Event

1. Click **Test**.
2. Configure:

```text
Event Name: CleanupTest
```

3. Use the default payload:

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

* Scan all objects in the bucket.
* Identify objects older than 30 days.
* Delete those objects.
* Log deleted object names in CloudWatch.

---

# Step 9: Verify Results in S3

Navigate to:

```text
Amazon S3 → Your Bucket
```

Verify:

* Files older than 30 days have been deleted.
* Files newer than 30 days remain in the bucket.

---

# Step 10: Verify CloudWatch Logs

1. Open **Amazon CloudWatch**.
2. Navigate to:

```text
Log Groups
```

3. Open:

```text
/aws/lambda/S3-Bucket-Cleanup
```

Example logs:

```text
Deleted: file1.txt
Deleted: file2.pdf
Deleted: old_backup.zip
```

---

# Expected Output

Example Lambda Response:

```json
{
  "statusCode": 200,
  "deleted_files": [
    "file1.txt",
    "file2.pdf",
    "old_backup.zip"
  ]
}
```

---

# Project Structure

```text
Assignment-2/
│
├── README.md
└── lambda_function.py
```

---

# Services Used

* Amazon S3
* AWS Lambda
* AWS IAM
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

# Workflow

```text
Upload Files to S3
        │
        ▼
Invoke Lambda Function
        │
        ▼
List All Objects
        │
        ▼
Check Last Modified Date
        │
        ▼
Delete Files Older Than 30 Days
        │
        ▼
Log Deleted Files in CloudWatch
```

---

# Learning Outcomes

After completing this assignment, you will be able to:

* Create and manage S3 buckets.
* Upload and organize objects in Amazon S3.
* Configure IAM roles and permissions.
* Develop AWS Lambda functions using Python.
* Use Boto3 to interact with S3 resources.
* Automate file lifecycle management.
* Monitor Lambda execution using CloudWatch logs.

---

# Best Practices

* Use IAM least-privilege policies in production.
* Enable S3 Versioning before deleting important files.
* Test Lambda functions in a non-production environment.
* Monitor logs regularly using CloudWatch.
* Consider using S3 Lifecycle Policies for large-scale cleanup operations.

---

# Author

**AWS Lambda & Boto3 - Automated S3 Bucket Cleanup Assignment**
