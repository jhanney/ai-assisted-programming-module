import re

PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

for address in ['a@b..com', '"john doe"@example.com']:
    print(address, '->', bool(re.match(PATTERN, address)))
