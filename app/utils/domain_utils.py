import re
from typing import Optional
from urllib.parse import urlparse


def validate_domain_name(domain_name: str) -> Optional[str]:
    domain_name = clean_domain_name(domain_name)
    return domain_name if is_valid_domain(domain_name) else None


def clean_domain_name(domain_name: str) -> str:
    # Remove http://, https://, and www.
    parsed_url = urlparse(domain_name)
    if parsed_url.scheme:
        domain_name = parsed_url.netloc
    else:
        domain_name = parsed_url.path

    domain_name = re.sub(r'^www\.', '', domain_name).strip().lower()
    return domain_name


def is_valid_domain(domain_name: str) -> bool:
    """
    Checks if a given domain name is valid according to ICANN rules.

    Args:
        domain_name (str): The domain name to be checked.

    Returns:
        bool: True if the domain name is valid, False otherwise.
    """
    # Define regular expressions for valid domain names
    domain_regex = r'^((?!-)[a-z0-9-]{1,63}(?<!-)\.)+[a-z]{2,6}$'
    hostname_regex = r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$'

    # Check if the domain name matches the regular expressions
    if re.match(domain_regex, domain_name) and re.match(hostname_regex, domain_name.split('.')[-2]):
        return True
    else:
        return False
