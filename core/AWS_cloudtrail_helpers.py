import boto3
from datetime import date, timedelta, datetime

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

