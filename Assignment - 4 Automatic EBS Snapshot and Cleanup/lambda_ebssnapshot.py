import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

# Replace with your volume ID
VOLUME_ID = 'vol-0abc123456789xyz'


def lambda_handler(event, context):

    # ---------------------------
    # Create Snapshot
    # ---------------------------

    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated Lambda Snapshot'
    )

    snapshot_id = snapshot['SnapshotId']

    print(f"Created Snapshot: {snapshot_id}")

    deleted_snapshots = []

    # ---------------------------
    # Find Old Snapshots
    # ---------------------------

    snapshots = ec2.describe_snapshots(
        OwnerIds=['self']
    )

    for snap in snapshots['Snapshots']:

        snapshot_age = (
            datetime.now(timezone.utc)
            - snap['StartTime']
        )

        if snapshot_age > timedelta(days=30):

            ec2.delete_snapshot(
                SnapshotId=snap['SnapshotId']
            )

            deleted_snapshots.append(
                snap['SnapshotId']
            )

            print(
                f"Deleted Snapshot: "
                f"{snap['SnapshotId']}"
            )

    return {
        'statusCode': 200,
        'created_snapshot': snapshot_id,
        'deleted_snapshots': deleted_snapshots
    }