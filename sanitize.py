def sanitize_message(data):
    """
    Sanitize boolean values in the dictionary to their string equivalents.
    """
    for key, value in data.items():
        if not isinstance(value, str):
            data[key] = str(value)
    
    return data
