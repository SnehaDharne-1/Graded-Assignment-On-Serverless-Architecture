# Assignment 8: Analyze Sentiment of User Reviews Using AWS Lambda, Boto3, and Amazon Comprehend

## Objective

The objective of this assignment is to automatically analyze and categorize the sentiment of user reviews using Amazon Comprehend. AWS Lambda receives user reviews, processes them through Amazon Comprehend, and logs the sentiment analysis results.

---

# Architecture Overview

```text
User Review Event
        │
        ▼
   AWS Lambda
        │
        ▼
 Amazon Comprehend
        │
        ▼
 Sentiment Analysis
        │
        ▼
 CloudWatch Logs
```

---

# Prerequisites

Before starting, ensure you have:

* AWS Account
* Access to:

  * AWS Lambda
  * Amazon Comprehend
  * AWS IAM
  * Amazon CloudWatch
* Basic knowledge of Python and AWS services

---

# Step 1: Create IAM Role for Lambda

## Create Role

1. Open the AWS IAM Console.
2. Navigate to **Roles → Create Role**.
3. Select:

   * Trusted Entity Type: **AWS Service**
   * Use Case: **Lambda**
4. Click **Next**.

---

## Attach Permissions

Attach the following policies:

```text
ComprehendFullAccess
```

```text
AWSLambdaBasicExecutionRole
```

> Note: For production environments, create a custom IAM policy with least-privilege permissions instead of using full access.

---

## Role Name

```text
Lambda-Comprehend-Role
```

Click **Create Role**.

---

# Step 2: Create Lambda Function

## Create Function

1. Open the AWS Lambda Console.
2. Click **Create Function**.
3. Select **Author from Scratch**.

### Configuration

| Setting        | Value                     |
| -------------- | ------------------------- |
| Function Name  | Review-Sentiment-Analyzer |
| Runtime        | Python 3.x                |
| Architecture   | x86_64                    |
| Execution Role | Use Existing Role         |
| IAM Role       | Lambda-Comprehend-Role    |

Click **Create Function**.

---

# Step 3: Lambda Function Code

Replace the default Lambda code with the following:

```python
import json
import boto3

comprehend = boto3.client('comprehend')

def lambda_handler(event, context):

    review = event['review']

    response = comprehend.detect_sentiment(
        Text=review,
        LanguageCode='en'
    )

    sentiment = response['Sentiment']

    print(f"Review: {review}")
    print(f"Sentiment: {sentiment}")

    return {
        'statusCode': 200,
        'review': review,
        'sentiment': sentiment
    }
```

---

# Step 4: Deploy Lambda Function

1. Click **Deploy**.
2. Wait until deployment completes successfully.

---

# Step 5: Create Test Event

1. Click **Test**.
2. Configure:

```text
Event Name: PositiveReviewTest
```

3. Use the following JSON payload:

```json
{
  "review": "This product is amazing. I really enjoyed using it and would highly recommend it."
}
```

4. Save the test event.

---

# Step 6: Test the Lambda Function

Click:

```text
Test
```

The Lambda function will:

1. Read the review from the event.
2. Send the review text to Amazon Comprehend.
3. Analyze the sentiment.
4. Log the result in CloudWatch.
5. Return the sentiment in the response.

---

# Step 7: Test Different Sentiments

## Positive Review

```json
{
  "review": "The service was excellent and the staff was very helpful."
}
```

Expected Result:

```text
POSITIVE
```

---

## Negative Review

```json
{
  "review": "I am very disappointed with this product. It stopped working after one day."
}
```

Expected Result:

```text
NEGATIVE
```

---

## Neutral Review

```json
{
  "review": "The product arrived yesterday. It is available in black color."
}
```

Expected Result:

```text
NEUTRAL
```

---

## Mixed Review

```json
{
  "review": "The design is great but the battery life is terrible."
}
```

Expected Result:

```text
MIXED
```

---

# Step 8: Verify CloudWatch Logs

1. Open **Amazon CloudWatch**.
2. Navigate to:

```text
Log Groups
```

3. Open:

```text
/ aws / lambda / Review-Sentiment-Analyzer
```

Example Logs:

```text
Review: This product is amazing. I really enjoyed using it and would highly recommend it.

Sentiment: POSITIVE
```

---

# Expected Output

Example Lambda Response:

```json
{
  "statusCode": 200,
  "review": "This product is amazing. I really enjoyed using it and would highly recommend it.",
  "sentiment": "POSITIVE"
}
```

---

# Project Structure

```text
Assignment-8/
│
├── README.md
└── lambda_function.py
```

---

# Services Used

* AWS Lambda
* Amazon Comprehend
* Amazon CloudWatch
* AWS IAM
* Boto3 (AWS SDK for Python)

---

# Workflow

```text
User Review
     │
     ▼
AWS Lambda
     │
     ▼
Amazon Comprehend
     │
     ▼
Detect Sentiment
     │
     ▼
CloudWatch Logs
```

---

# Learning Outcomes

After completing this assignment, you will be able to:

* Create and configure AWS Lambda functions.
* Use Amazon Comprehend for Natural Language Processing (NLP).
* Analyze sentiment from text data.
* Integrate AWS services using Boto3.
* Process event-driven data in Lambda.
* Monitor Lambda execution using CloudWatch Logs.

---

# Best Practices

* Use least-privilege IAM policies.
* Validate incoming event data.
* Store configuration values in environment variables.
* Enable CloudWatch monitoring and alerts.
* Handle exceptions gracefully in production code.
* Consider API Gateway integration for real-world applications.

---

# Submission Requirements

Include the following in your submission:

### Python Code

* Lambda function source code (`lambda_function.py`)

### Screenshots

* Lambda Function Configuration
* Successful Test Execution
* CloudWatch Logs Showing Sentiment Results

### Documentation

* README.md file
* Steps followed during implementation

---

# Author

**AWS Lambda, Boto3, and Amazon Comprehend – Sentiment Analysis Assignment**

Serverless Architecture Graded Assignment
