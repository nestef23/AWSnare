import boto3
from botocore.exceptions import ClientError
from datetime import date, timedelta, datetime
import uuid

from core import config_helpers
from core import AWS_S3_helpers
from core import detection_logic

default_region = config_helpers.default_region_get()
all_regions = config_helpers.regions_get()
AWSnare_tag = config_helpers.AWSnare_tag_get()
cloudtrail_trail_name = config_helpers.cloudtrail_name_get()
account_id = config_helpers.account_id_get()

def detect_cloudtrail_events_locally():
    """Detect any activity regarding the snares that are set up"""

    trail_region = input(f"Region where trail is located (default: {default_region}) ").strip() or default_region
    client = boto3.client('cloudtrail', region_name=trail_region)

    trail_name = input(f"Enter the name of the configured trail: (default: {cloudtrail_trail_name}) ").strip() or cloudtrail_trail_name
    response = client.get_trail(Name=trail_name)
    S3_bucket_name = response['Trail']['S3BucketName']

    start_date_tmp = date.today() - timedelta(days=7)
    user_input = input(f"Detection start date (YYYY-MM-DD, default: {start_date_tmp}): ").strip()
    if user_input:
            start_date = datetime.strptime(user_input, "%Y-%m-%d").date()
    else:
        start_date = start_date_tmp
    end_date = date.today()

    print(f"Downloading Cloudtrail logs from bucket {S3_bucket_name} for configured regions {all_regions}")

    AWS_S3_helpers.download_cloudtrail_logs(S3_bucket_name, account_id, all_regions, start_date, end_date)

    detection_logic.detect_cloudtrail()

def update_selectors(trail_region, trail_name):
    ARN_list = config_helpers.AWS_snares_arn_list_get()

    client = boto3.client('cloudtrail', region_name=trail_region)
    print(f"[+] Configuring data event selectors for Cloudtrail...")
    client.put_event_selectors(
        TrailName=trail_name,
        EventSelectors=[
            {
                "ReadWriteType": "All",  # or 'ReadOnly' / 'WriteOnly'
                "IncludeManagementEvents": False,  # No management events
                "DataResources": [
                    {
                        "Type": "AWS::S3::Object",  # or AWS::Lambda::Function
                        "Values": [r+"/*" for r in ARN_list if ":s3:::" in r]
                    },
                    {
                        "Type": "AWS::Lambda::Function",
                        "Values": [r for r in ARN_list if ":lambda:" in r]
                    }
                ]
            }
        ]
    )

def create_cloudtrail_trail():
    """Create cloudtrail trail where snare logs will be stored."""

    print("This function will create a new CloudTrail trail and respective S3 bucket for logs\n")

    trail_region = input(f"Region where trail will be created (default: {default_region}) ").strip() or default_region
    client = boto3.client('cloudtrail', region_name=trail_region)

    random_suffix = uuid.uuid4().hex[:8]
    trail_name = (input(f"New trail name (default: {AWSnare_tag}-{random_suffix}) ").strip() or AWSnare_tag+"-"+random_suffix).lower()
    trail_bucket_name = (input(f"New trail bucket name (default: {trail_name}-bucket):" ).strip() or trail_name+"-bucket").lower()

    AWS_S3_helpers.create_s3_bucket(False, trail_bucket_name, trail_region)

    AWS_S3_helpers.attach_bucket_policy(trail_bucket_name, account_id)

    try:
        response = client.create_trail(
        Name=trail_name,
        S3BucketName=trail_bucket_name,
        #SnsTopicName='string', TODO implement SNS?
        IncludeGlobalServiceEvents=False,
        IsMultiRegionTrail=False,
        IsOrganizationTrail=False,
        TagsList=[
            {
                'Key': AWSnare_tag,
                'Value': 'true'
            }
        ]
        )
        print(f"[+] Trail {trail_name} created successfully.")
    except ClientError as e:
        print(f"[!] Error creating trail: {e}")

    update_selectors(trail_region, trail_name)

    config_helpers.cloudtrail_name_set(trail_name)

    print(f"[+] Starting logging for {trail_name}")
    client.start_logging(Name=trail_name)
