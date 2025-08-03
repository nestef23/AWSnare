import yaml
from typing import List

SETTINGLS_FILE = "config.yaml"

AWS_regions = ["us-east-1","us-east-2","us-west-1","us-west-2","af-south-1","ap-east-1","ap-south-2","ap-southeast-3","ap-southeast-5","ap-southeast-4","ap-south-1","ap-northeast-3","ap-northeast-2","ap-southeast-1","ap-southeast-2","ap-east-2","ap-southeast-7","ap-northeast-1","ca-central-1","ca-west-1","eu-central-1","eu-west-1","eu-west-2","eu-south-1","eu-west-3","eu-south-2","eu-north-1","eu-central-2","il-central-1","mx-central-1","me-south-1","me-central-1","sa-east-1"]

def load_settings():
    try:
        with open(SETTINGLS_FILE, "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}

def save_settings(settings):
    with open(SETTINGLS_FILE, "w") as f:
        yaml.dump(settings, f, default_flow_style=False)

def config_print():
    """Print current configuration settings."""
    print("Current configuration settings:\n")
    settings = load_settings()
    print(yaml.dump(settings, default_flow_style=False, sort_keys=False))

def AWSnare_tag_get():
    """Get the AWSnare tag."""
    settings = load_settings()
    if "AWSnare_tag" in settings:
        return settings["AWSnare_tag"]
    else:
        return "No configured AWSnare tag found. Please configure tag first"

def default_region_set():
    """Set the default AWS region."""
    settings = load_settings()

    while True:
        def_region = input("\nEnter new default AWS region (e.g., us-east-1): ").strip().lower()

        if def_region in AWS_regions:
            settings["AWS_default_region"] = def_region
            print(f"Default region set to: {def_region}")
            break
        elif def_region == "exit":
            print("Exiting without changes.")
            return
        else:
            print("\nInvalid AWS region. Please enter a valid region from the following list:")
            print(", ".join(AWS_regions))

    save_settings(settings)

def default_region_get():
    settings = load_settings()
    if "AWS_default_region" in settings:
        return settings["AWS_default_region"]
    else:
        return "No configured default region found. Please configure region first"

def regions_get():
    settings = load_settings()
    if "AWS_configured_regions" in settings:
        return settings["AWS_configured_regions"]
    else:
        return ["No configured default region found. Please configure region first"]

def cloudtrail_name_get():
    settings = load_settings()
    if "AWS_cloudtrail_name" in settings:
        return settings["AWS_cloudtrail_name"]
    else:
        return "No configured Cloudtrail. Please configure / create trail first."

def cloudtrail_name_set(trail_name):
    settings = load_settings()

    settings["AWS_cloudtrail_name"] = trail_name

    save_settings(settings)

def account_id_get():
    settings = load_settings()
    if "AWS_account_id" in settings:
        return settings["AWS_account_id"]
    else:
        return "No configured account id. Please configure account id first"

def AWS_snares_arn_list_get() -> List:
    settings = load_settings()
    try:
        return settings["AWS_snares_arn_list"]
    except:
        print("No configured account id. Please configure account id first")
        return []

def AWS_snares_arn_list_add(arn: str):
    settings = load_settings()

    # Initialize the list if it doesn't exist
    if "AWS_snares_arn_list" not in settings:
        settings["AWS_snares_arn_list"] = []

    settings["AWS_snares_arn_list"].append(arn)
    save_settings(settings)

def AWS_snares_arn_list_remove(arn: str):
    settings = load_settings()

    settings["AWS_snares_arn_list"].remove(arn)
    save_settings(settings)

def regions_add():
    """Add AWS region to AWS_all_regions."""
    settings = load_settings()
    # Initialize the list if it doesn't exist
    if "AWS_configured_regions" not in settings:
        settings["AWS_configured_regions"] = []

    while True:
        new_region = input("Enter new AWS region to add (e.g., us-east-1): ").strip().lower()

        if new_region in AWS_regions:
            if new_region not in settings["AWS_configured_regions"]:
                settings["AWS_configured_regions"].append(new_region)
                print(f"✅ Region '{new_region}' added.")
                break
            else:
                print("\nInvalid AWS region. Please enter a valid region from the following list:")
                print(", ".join(AWS_regions))
        elif new_region == "exit":
            print("Exiting without changes.")
            return
        else:
            print("\nInvalid AWS region. Please enter a valid region from the following list:")
            print(", ".join(AWS_regions))

    save_settings(settings)

def regions_remove():
    settings = load_settings()

    rm_region = input("Enter AWS region to remove (e.g., us-east-1): ").strip().lower()

    if "AWS_configured_regions" in settings and rm_region in settings["AWS_configured_regions"]:
        settings["AWS_configured_regions"].remove(rm_region)
        print(f"🗑️ Region '{rm_region}' removed.")
    else:
        print(f"⚠️ Region '{rm_region}' not found in list.")

    save_settings(settings)
