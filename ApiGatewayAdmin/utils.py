import bleach
import re

# Global sanitization function
def sanitize_data(data):
    """
    Sanitize incoming request data by removing potentially harmful characters (strings or JSON).
    Returns sanitized data ready to be forwarded to microservices.
    Should be used to sanitize the request body (JSON data) before forwarding it to the target microservice.
    """
    if isinstance(data, str):
        # Check for SQL injection patterns and remove them
        data = re.sub(r"(;|--|\|{2}|&&|`)", "", data)  # Remove common SQL/command injection characters
        data = re.sub(r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER)\b)", "", data, flags=re.IGNORECASE)  # Removes SQL keywords
        
        # Sanitize the string using bleach
        return bleach.clean(data)
    elif isinstance(data, dict):
        sanitized_data = {}
        for key, value in data.items():
            sanitized_data[key] = sanitize_data(value) if isinstance(value, (str, dict)) else value
        return sanitized_data
    return data