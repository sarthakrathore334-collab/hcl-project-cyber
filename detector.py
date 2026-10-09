def detect_xss(text):

    patterns = {
        "<script": "High",
        "javascript:": "High",
        "document.cookie": "High",
        "onerror=": "Medium",
        "onload=": "Medium",
        "onclick=": "Medium",
        "<iframe": "Medium",
        "<svg": "Medium"
    }

    text = text.lower()

    for pattern, severity in patterns.items():
        if pattern in text:
            return True, pattern, severity

    return False, None, None