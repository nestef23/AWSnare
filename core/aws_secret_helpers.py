import boto3
from botocore.exceptions import ClientError
import os
import json
import gzip
from datetime import timedelta
import uuid

from core import config_helpers
from core import random_helpers

default_region = config_helpers.default_region_get()
all_regions = config_helpers.regions_get()
AWSnare_tag = config_helpers.AWSnare_tag_get()

def get_secrets_names():
    """Retrieve a list of secrets from Secrets manager."""

    print(f"[+] Fetching secrets with tag: '{AWSnare_tag}'...")

    for region_name in all_regions:
        session = boto3.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
        )

        response = client.list_secrets(Filters=[{'Key': 'tag-key', 'Values': [AWSnare_tag]}])

        print(f"Secrets in region {region_name}:")
        for secret in response['SecretList']:
            print(f" - Secret Name: {secret['Name']}, Description: {secret['Description']}, ARN: {secret['ARN']}")

def create_secret(snare: bool, secret_name = "", chosen_region = ""):
    """Create a new secret in SecretsManager"""

    tmp_name = random_helpers.generate_aws_resource_name()

    if not secret_name:
        secret_name = input(f"Enter the name for the new S3 bucket: (default: {tmp_name}) ").strip() or tmp_name
    if not chosen_region:
        chosen_region = input(f"Enter the region for the new S3 bucket (default: {default_region}): ").strip() or default_region

    client = boto3.client('secretsmanager', region_name=chosen_region)

    # Create the bucket first
    try:
        response = client.create_secret(
            Name=secret_name,
            Description=secret_name,
            SecretString=str(uuid.uuid4()),
            Tags=[
                {
                    'Key': AWSnare_tag,
                    'Value': 'true'
                },
            ]
        )
        print(f"[+] Secret '{secret_name}' created successfully.")
    except ClientError as e:
        raise RuntimeError("[!] Error creating secret: {e}")

    if snare:
        arn = response['ARN']
        print(f"[+] Added arn '{arn}' to the snares list")
        config_helpers.AWS_snares_arn_list_add(arn)