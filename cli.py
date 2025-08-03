import argparse

from core import AWS_S3_helpers  # Importing the helper functions
from core import AWS_secret_helpers
from core import AWS_cloudtrail_helpers 
from core import config_helpers
from core import detection_logic

# -----------------------------
# Handlers for each command
# -----------------------------

def handle_get(args):
    if args.resource == "S3":
        AWS_S3_helpers.get_s3_bucket_names()
    elif args.resource == "secret":
        AWS_secret_helpers.get_secrets_names()
    else:
        print(f"Unsupported resource for get: {args.resource}")

def handle_create(args):
    if args.resource == "S3":
        AWS_S3_helpers.create_s3_bucket(snare=True)
    elif args.resource == "secret":
        AWS_secret_helpers.create_secret(snare=True)
    else:
        print(f"Unsupported resource for create: {args.resource}")

def handle_delete(args):
    if args.resource == "s3":
        print("Deleting S3 resource...")
        # your_function_to_delete_s3()
    else:
        print(f"Unsupported resource for delete: {args.resource}")

def handle_config(args):
    if args.setting == "show":
        config_helpers.config_print()
    elif args.setting == "def_reg":
        config_helpers.default_region_set() 
    elif args.setting == "add_reg":
        config_helpers.regions_add()
    elif args.setting == "rm_reg":
        config_helpers.regions_remove()
    else:
        print(f"Unsupported setting for config: {args.setting}")

def handle_detect(args):
    if args.method == "setup":
        AWS_cloudtrail_helpers.create_cloudtrail_trail()
    elif args.method == "update":
        AWS_cloudtrail_helpers.update_selectors()
    elif args.method == "run-local":
        AWS_cloudtrail_helpers.detect_cloudtrail_events_locally()
    else:
        print(f"Unsupported values for detect: {args.method}")

# -----------------------------
# CLI Setup
# -----------------------------

def main():
    parser = argparse.ArgumentParser(description='AWSnare CLI - Manage AWS snares and monitor logs')
    subparsers = parser.add_subparsers(dest='command', required=True)

    AWS_resource_types = ['S3', 'secret', 'IAM_account', 'lambda', 'EC2_key_pair']

    # Get command
    get_parser = subparsers.add_parser('get', help="List existing snares")
    get_parser.add_argument('resource', choices = AWS_resource_types, help="Snare type to list")
    get_parser.set_defaults(func=handle_get)

    # Create command
    create_parser = subparsers.add_parser('create', help="Create a new snare")
    create_parser.add_argument('resource', choices = AWS_resource_types, help="Snare type to create")
    create_parser.set_defaults(func=handle_create)

    # Delete command
    delete_parser = subparsers.add_parser('delete', help="Delete existing snare")
    delete_parser.add_argument('resource', choices = AWS_resource_types, help="Snare type to delete")
    delete_parser.set_defaults(func=handle_delete)

    # config command
    config_parser = subparsers.add_parser('config', help="Configure your default settings")
    config_parser.add_argument('setting', choices=['show', 'def_reg', 'add_reg', 'rm_reg'], help="Setting to configure")
    config_parser.set_defaults(func=handle_config)

    # detect command
    config_parser = subparsers.add_parser('detect', help="Detect activity in the snares")
    config_parser.add_argument('method', choices=['setup','update','run-local'], help="Detection method")
    config_parser.set_defaults(func=handle_detect)

    # Parse and dispatch
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()