import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 's3-cleanup-assignment-sneha'


def lambda_handler(event, context):

    objects = s3.list_objects_v2(
        Bucket=BUCKET_NAME
    )

    deleted_files = []

    if 'Contents' in objects:

        for obj in objects['Contents']:

            file_name = obj['Key']
            last_modified = obj['LastModified']

            age = datetime.now(
                timezone.utc
            ) - last_modified

            if age > timedelta(days=30):

                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=file_name
                )

                deleted_files.append(file_name)

                print(
                    f"Deleted: {file_name}"
                )

    return {
        "statusCode": 200,
        "deleted_files": deleted_files
    }