
VERSION = "1.0.0"
from typing import List

def get_messages() -> List[str]:
    messages = []
    for i in range(0, 100):
        messages.append(f"message:{VERSION}:{i}")
    return messages
