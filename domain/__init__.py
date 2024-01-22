import re


def validate_domain(domain: str) -> bool:
    pattern = r'^(?!:\/\/)(?:[-A-Za-z0-9]+\.)+[A-Za-z]{2,6}$'

    if re.match(pattern, domain):
        return True
    else:
        return False
