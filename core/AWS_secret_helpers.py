import boto3

from core import config_helpers

default_region = config_helpers.default_region_get()
all_regions = config_helpers.regions_get()
AWSnare_tag = config_helpers.AWSnare_tag_get()

def get_secrets_names():
    """Retrieve a list of secrets from Secrets manager."""

    print(f"Fetching secrets with tag: '{AWSnare_tag}'...")

    for region_name in all_regions:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
        )

        response = client.list_secrets(Filters=[{'Key': 'tag-key', 'Values': [AWSnare_tag]}])

        print(f"Secrets in region {region_name}:")
        for secret in response['SecretList']:
            print(f" - Secret Name: {secret['Name']}, Description: {secret['Description']}, ARN: {secret['ARN']}")