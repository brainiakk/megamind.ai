from functools import wraps
import requests

def internet_tool(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Try to reach a known online host
            requests.get("http://www.google.com", timeout=2)
            return func(*args, **kwargs)  # Call the tool if online
        except (requests.ConnectionError, requests.Timeout):
            return "Sorry, I seem to be having trouble accessing the internet right now."
    return wrapper
