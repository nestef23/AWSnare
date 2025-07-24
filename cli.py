import argparse
import sys
from core import aws_helpers  # Importing the helper functions

# -----------------------------
# Handlers for each command
# -----------------------------

def handle_get(args):
    if args.resource == "s3":
        print("Fetching S3 resources...")
        aws_helpers.get_s3_bucket_names()  # Call the function to get S3 bucket names
    elif args.resource == "ec2":
        print("Fetching EC2 resources...")
        # your_function_to_get_ec2()
    else:
        print(f"Unsupported resource for get: {args.resource}")

def handle_create(args):
    if args.resource == "iam":
        print("Creating IAM resource...")
        # your_function_to_create_iam()
    else:
        print(f"Unsupported resource for create: {args.resource}")

def handle_delete(args):
    if args.resource == "s3":
        print("Deleting S3 resource...")
        # your_function_to_delete_s3()
    else:
        print(f"Unsupported resource for delete: {args.resource}")

# -----------------------------
# CLI Setup
# -----------------------------

def main():
    parser = argparse.ArgumentParser(description='AWSnare CLI - Manage AWS honeypots and monitor logs')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Get command
    get_parser = subparsers.add_parser('get', help="Get a resource")
    get_parser.add_argument('resource', choices=['s3', 'ec2', 'iam'], help="Resource to get")
    get_parser.set_defaults(func=handle_get)

    # Create command
    create_parser = subparsers.add_parser('create', help="Create a resource")
    create_parser.add_argument('resource', choices=['s3', 'ec2', 'iam'], help="Resource to create")
    create_parser.set_defaults(func=handle_create)

    # Delete command
    delete_parser = subparsers.add_parser('delete', help="Delete a resource")
    delete_parser.add_argument('resource', choices=['s3', 'ec2', 'iam'], help="Resource to delete")
    delete_parser.set_defaults(func=handle_delete)

    # Parse and dispatch
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()