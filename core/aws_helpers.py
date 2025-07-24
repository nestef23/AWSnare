import boto3

def get_s3_bucket_names():
    """Retrieve a list of S3 bucket names."""
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # Output the bucket names
    if len(response['Buckets']) == 0:
        print("No S3 buckets found.")
    else:
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')