import boto3
from botocore.exceptions import ClientError
import os
import json
import gzip
from datetime import timedelta

from core import config_helpers
from core import random_helpers


default_region = config_helpers.default_region_get()
all_regions = config_helpers.regions_get()
AWSnare_tag = config_helpers.AWSnare_tag_get()

def get_s3_bucket_names():
    """Retrieve a list of S3 bucket names."""

    print(f"Fetching S3 buckets with tag: '{AWSnare_tag}'...")

    s3 = boto3.client('s3')

    # List all buckets
    buckets = s3.list_buckets()

    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        try:
            tagging = s3.get_bucket_tagging(Bucket=bucket_name)
            tag_set = tagging['TagSet']
            if any(tag['Key'] == AWSnare_tag for tag in tag_set):
                print (bucket_name)
        except ClientError as e:
            # Ignore buckets with no tags or access denied
            if e.response['Error']['Code'] != 'NoSuchTagSet':
                print(f"Error getting tags for {bucket_name}: {e}")

def create_s3_bucket():
    """Create a new S3 bucket."""

    tmp_name = random_helpers.generate_aws_resource_name()

    bucket_name = input(f"Enter the name for the new S3 bucket: (default: {tmp_name}) ").strip() or tmp_name
    chosen_region = input(f"Enter the region for the new S3 bucket (default: {default_region}): ").strip() or default_region

    s3 = boto3.client('s3')

    # Create the bucket first
    try:
        if chosen_region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                'LocationConstraint': chosen_region
            })
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating S3 bucket: {e}")

    # Apply tags separately
    try:
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {'Key': AWSnare_tag, 'Value': 'true'}
                ]
            }
        )
        print(f"Tag '{AWSnare_tag}' added to S3 bucket '{bucket_name}'.")
    except ClientError as e:
        print(f"Error applying tags to S3 bucket: {e}")

def download_cloudtrail_logs(bucket_name, account_id, regions, start_date, end_date):
    """
    Downloads CloudTrail logs for multiple dates and regions.
    start_date / end_date: datetime.date objects
    regions: list of AWS region strings
    """

    s3 = boto3.client('s3')

    download_dir = 'logs_cloudtrail'

    current_date = start_date
    while current_date <= end_date:
        for region in regions:
            prefix = f"AWSLogs/{account_id}/CloudTrail/{region}/{current_date.year}/{current_date.month:02}/{current_date.day:02}/"

            paginator = s3.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
                for obj in page.get("Contents", []):
                    key = obj["Key"]
                    filename = key.split("/")[-1]
                    local_path = os.path.join(download_dir, f"{region}_{current_date}_{filename}")

                    print(f"[{current_date} - {region}] Downloading {key}...")
                    s3.download_file(bucket_name, key, local_path)

                    # Optional: Parse logs immediately
                    with gzip.open(local_path, "rt") as f:
                        log_data = json.load(f)
                        print(f"  → {len(log_data['Records'])} events")

        current_date += timedelta(days=1)
    print("Finished downloading logs")