def is_valid_email(address: str) -> bool:
    """Return whether address has an @ and a dot after it."""
    if len(address) > 254:
        return False

    at_index = address.find("@")
    return at_index != -1 and "." in address[at_index + 1:]
