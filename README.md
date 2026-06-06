# Graded-Assignment-On-Serverless-Architecture

## Overview

This repository contains the implementation of multiple AWS Serverless Architecture assignments using AWS Lambda, Boto3, Amazon SNS, Amazon DynamoDB, Amazon S3, Amazon EC2, Amazon Comprehend, Amazon EventBridge, and Amazon CloudWatch.

The goal of these assignments is to gain hands-on experience with serverless computing, event-driven architecture, automation, monitoring, and cloud resource management on AWS.

---

# Objectives

- Understand AWS Lambda and serverless architecture.
- Automate AWS infrastructure management.
- Implement event-driven workflows.
- Integrate AWS services using Boto3.
- Monitor resources and generate alerts.
- Apply cost optimization and automation techniques.
- Gain practical experience with AWS cloud services.

---

# Technologies Used

- AWS Lambda
- Amazon EC2
- Amazon EBS
- Amazon S3
- Amazon DynamoDB
- DynamoDB Streams
- Amazon SNS
- Amazon Comprehend
- Amazon EventBridge (CloudWatch Events)
- Amazon CloudWatch
- AWS IAM
- Python 3.x
- Boto3 (AWS SDK for Python)

---

# Repository Structure

```text
Graded-Assignment-On-Serverless-Architecture/
│
├── Assignment-1-EC2-Auto-Management/
│   ├── README.md
│   └── lambda_function.py
│
├── Assignment-2-S3-Bucket-Cleanup/
│   ├── README.md
│   └── lambda_function.py
│
├── Assignment-4-EBS-Snapshot-Cleanup/
│   ├── README.md
│   └── lambda_function.py
│
├── Assignment-5-EC2-Auto-Tagging/
│   ├── README.md
│   └── lambda_function.py
│
├── Assignment-6-AWS-Billing-Monitor/
│   ├── README.md
│   └── lambda_function.py
│
├── Assignment-7-DynamoDB-Change-Alert/
│   ├── README.md
│   ├── lambda_function.py
│   └── screenshots/
│
├── Assignment-8-Sentiment-Analysis-Comprehend/
│   ├── README.md
│   └── lambda_function.py
│
└── README.md
```

---

# Assignments Completed

## Assignment 1: Automated EC2 Instance Management Using AWS Lambda and Boto3

### Objective

Automatically start and stop EC2 instances based on predefined tags.

### AWS Services Used

- Amazon EC2
- AWS Lambda
- AWS IAM
- Amazon CloudWatch
- Boto3

### Features

- Detect EC2 instances tagged as `Auto-Start`
- Start stopped instances automatically
- Detect EC2 instances tagged as `Auto-Stop`
- Stop running instances automatically
- Log actions in CloudWatch

### Learning Outcomes

- Managing EC2 instances programmatically
- Using EC2 APIs through Boto3
- Automating infrastructure tasks using Lambda

---

## Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

### Objective

Automatically delete files older than 30 days from an S3 bucket.

### AWS Services Used

- Amazon S3
- AWS Lambda
- AWS IAM
- Amazon CloudWatch
- Boto3

### Features

- Scan bucket contents
- Identify old objects
- Delete objects older than 30 days
- Maintain clean and optimized storage

### Learning Outcomes

- Working with S3 buckets and objects
- Automating storage management
- Using timestamps and lifecycle logic

---

## Assignment 4: Automatic EBS Snapshot and Cleanup

### Objective

Create EBS snapshots automatically and remove backups older than 30 days.

### AWS Services Used

- Amazon EBS
- Amazon EC2
- AWS Lambda
- EventBridge
- CloudWatch
- Boto3

### Features

- Automated EBS snapshot creation
- Snapshot retention policy
- Delete outdated snapshots
- Scheduled backup execution

### Learning Outcomes

- Managing EBS backups
- Implementing retention policies
- Automating disaster recovery processes

---

## Assignment 5: Auto-Tagging EC2 Instances on Launch

### Objective

Automatically tag newly launched EC2 instances.

### AWS Services Used

- Amazon EC2
- AWS Lambda
- EventBridge
- AWS IAM
- Boto3

### Features

- Detect EC2 launch events
- Apply launch date tag
- Apply custom environment tag
- Improve resource organization

### Learning Outcomes

- Event-driven architecture
- Automated resource tagging
- Cloud governance best practices

---

## Assignment 6: Monitor and Alert High AWS Billing

### Objective

Monitor AWS billing and notify users when charges exceed a predefined threshold.

### AWS Services Used

- Amazon CloudWatch
- AWS Lambda
- Amazon SNS
- EventBridge
- AWS IAM
- Boto3

### Features

- Retrieve billing metrics
- Compare against threshold value
- Send SNS email alerts
- Daily automated monitoring

### Learning Outcomes

- Cost monitoring automation
- Working with CloudWatch metrics
- SNS-based notifications

---

## Assignment 7: DynamoDB Item Change Alert

### Objective

Receive notifications whenever a DynamoDB item is modified.

### AWS Services Used

- Amazon DynamoDB
- DynamoDB Streams
- AWS Lambda
- Amazon SNS
- CloudWatch
- Boto3

### Features

- Capture item update events
- Extract old and new values
- Generate SNS notifications
- Real-time change tracking

### Learning Outcomes

- DynamoDB Streams integration
- Event-driven processing
- Database monitoring automation

---

## Assignment 8: Analyze Sentiment of User Reviews

### Objective

Automatically analyze user reviews and determine their sentiment using Amazon Comprehend.

### AWS Services Used

- Amazon Comprehend
- AWS Lambda
- CloudWatch
- AWS IAM
- Boto3

### Features

- Accept user review input
- Analyze sentiment using NLP
- Classify reviews as:
  - POSITIVE
  - NEGATIVE
  - NEUTRAL
  - MIXED
- Log sentiment results

### Learning Outcomes

- Natural Language Processing (NLP)
- Amazon Comprehend integration
- AI-powered serverless applications

---

# Architecture Pattern Used

```text
AWS Event / User Input
           │
           ▼
      AWS Lambda
           │
           ▼
      AWS Service
 (EC2/S3/DynamoDB/
 SNS/Comprehend)
           │
           ▼
   Business Logic
           │
           ▼
 CloudWatch Logs
```

---

# Deployment Steps

1. Create required AWS resources.
2. Create IAM roles and permissions.
3. Create Lambda functions.
4. Upload Python code.
5. Configure triggers and event sources.
6. Deploy Lambda functions.
7. Test functionality.
8. Verify logs and notifications.

---

# Skills Demonstrated

- Serverless Architecture
- AWS Lambda Development
- Event-Driven Computing
- Infrastructure Automation
- Cloud Monitoring
- Resource Management
- Backup Automation
- Cost Monitoring
- Notification Systems
- Natural Language Processing
- AWS Security and IAM
- Boto3 SDK Integration

---

# Screenshots Included

The repository contains screenshots demonstrating:

- Lambda Function Deployments
- EC2 Instance Automation
- S3 Cleanup Results
- EBS Snapshot Creation
- EC2 Auto-Tagging
- Billing Alert Emails
- SNS Notifications
- DynamoDB Streams
- CloudWatch Logs
- Amazon Comprehend Sentiment Analysis

---

# Future Enhancements

- Infrastructure as Code using Terraform
- AWS SAM Deployment
- CloudFormation Templates
- CI/CD Pipeline Integration
- Slack Notifications
- AWS Step Functions Integration
- Multi-Region Deployments
- Monitoring Dashboards

---

# Author

**Sneha Tandle**

Graded Assignment on Serverless Architecture using AWS Lambda, Boto3, Amazon SNS, Amazon DynamoDB, Amazon S3, Amazon EC2, Amazon Comprehend, EventBridge, and CloudWatch.

---

# License

This project is created for educational and learning purposes.
