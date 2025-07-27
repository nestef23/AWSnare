import random
import string

sensitive_keywords = [
    "secret", "hr", "finance", "vault", "credentials", "payroll", 
    "backup", "archive", "records", "audit", "reports", "token"
]

adjectives = [
    "internal", "prod", "secure", "confidential", "central", 
    "east", "west", "primary", "mirror", "compliance"
]

nouns = [
    "store", "bucket", "service", "db", "config", "access", 
    "data", "snapshot", "store", "cache", "pipeline", "repo"
]

def generate_aws_resource_name():
    """Generate a random AWS-compliant, human-readable resource name for honeytokens."""
    parts = [
        random.choice(sensitive_keywords),
        random.choice(adjectives),
        random.choice(nouns),
        ''.join(random.choices(string.digits, k=2))  # add a numeric suffix to make names unique
    ]
    name = '-'.join(parts).lower()
    
    # Truncate if exceeds 63 characters (e.g., for S3 buckets)
    return name[:63]

# Example usage
if __name__ == "__main__":
    for _ in range(10):
        print(generate_aws_resource_name())