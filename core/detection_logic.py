import gzip
import json
import os
import yaml
from typing import List, Dict, Any
from datetime import datetime

def load_rules_from_yaml(rules_file: str) -> List[Dict[str, Any]]:
    """Load detection rules from YAML."""
    with open(rules_file, "r") as f:
        rules_data = yaml.safe_load(f)
    return rules_data.get("rules", [])


def load_cloudtrail_file(filepath: str) -> List[Dict]:
    """Load and parse a gzipped CloudTrail log file."""
    with gzip.open(filepath, "rt") as f:
        data = json.load(f)
        return data.get("Records", [])


def event_matches_rule(event: Dict, logic: Dict[str, Any]) -> bool:
    """Check if a CloudTrail event matches a rule's logic."""
    for field, expected in logic.items():
        value = event.get(field)
        if isinstance(expected, list):
            if value not in expected:
                return False
        else:
            if value != expected:
                return False
    return True


def scan_file(filepath: str, rules: List[Dict[str, Any]]) -> List[Dict]:
    """Scan a single CloudTrail .gz file for rule matches."""
    events = load_cloudtrail_file(filepath)
    hits = []

    for event in events:
        for rule in rules:
            if event_matches_rule(event, rule["logic"]):
                hits.append(event)
                print(f"[{rule["name"]}]\n"
                    f"{rule["description"]}\n"
                    f"{event.get('eventTime')}\n"
                    f"eventName: {event.get('eventName')} "
                    f"sourceIPAddress: {event.get('sourceIPAddress')}\n"
                    f"userIdentity: {event.get("userIdentity", {}).get("arn")}\n"
                    f"resource: {event.get("resources", [])[0].get("ARN")}\n")
    return hits


def scan_directory(directory: str, rules: List[Dict[str, Any]]) -> List[Dict]:
    """Scan all .gz files in a directory."""
    all_hits = []
    print(f"Scanning {len(os.listdir(directory))} Cloudtrail files from '{directory}'... \n")
    for filename in os.listdir(directory):
        if filename.endswith(".gz"):
            filepath = os.path.join(directory, filename)
            all_hits.extend(scan_file(filepath, rules))
    return all_hits

def save_hits(hits: List[Dict], output_dir: str):
    """Save detection hits to a single JSON file in the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"detections_{timestamp}.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(hits, f, indent=2, ensure_ascii=False)
    
    return output_file

def detect_cloudtrail():

    print("\nAnalyzing logs\n")

    rules = load_rules_from_yaml("detection_rules.yaml")
    results = scan_directory("logs_cloudtrail", rules)

    if results:
        output_file = save_hits(results, "logs_detections")
        print(f"[+] Saved {len(results)} hits to {output_file}")