import requests


def analyze_reflection(url, parameter):

    marker = "XSS_TEST_123"
    probe = marker + "<test>"

    try:

        response = requests.get(
            url,
            params={parameter: probe},
            timeout=5
        )

        html = response.text

        # Check if the complete probe is reflected
        if probe in html:

            position = html.find(probe)

            start = max(0, position - 100)
            end = min(len(html), position + len(probe) + 100)

            snippet = html[start:end]

            return {
                "reflected": True,
                "context": "Raw HTML reflection",
                "severity": "High",
                "message": "The test input was reflected without HTML encoding.",
                "snippet": snippet
            }

        # Check if only the marker is reflected
        if marker in html:

            position = html.find(marker)

            start = max(0, position - 100)
            end = min(len(html), position + len(marker) + 100)

            snippet = html[start:end]

            return {
                "reflected": True,
                "context": "HTML-encoded reflection",
                "severity": "Low",
                "message": "The input was reflected but special characters appear to be encoded.",
                "snippet": snippet
            }

        return {
            "reflected": False,
            "context": "Not reflected",
            "severity": "None",
            "message": "The test input was not found in the response.",
            "snippet": ""
        }

    except requests.RequestException as e:

        return {
            "reflected": False,
            "context": "Connection error",
            "severity": "None",
            "message": "Could not connect to the target.",
            "snippet": str(e)
        }