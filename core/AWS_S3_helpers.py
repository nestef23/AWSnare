import boto3
from botocore.exceptions import ClientError

from core import config_helpers

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