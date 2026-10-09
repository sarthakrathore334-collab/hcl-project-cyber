"""
Intentionally vulnerable test server for XSS Guard scanner testing.
Runs on port 5001. DO NOT use in production — this reflects user input without sanitization.
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    # Intentionally reflects input without escaping (vulnerable to XSS)
    return f"""
    <html>
    <head><title>Test Search</title></head>
    <body>
        <h1>Search Results</h1>
        <p>You searched for: {query}</p>
        <p>No results found.</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    print("[!] Vulnerable test server running on http://127.0.0.1:5001")
    print("    This reflects input without sanitization - for testing only.")
    app.run(port=5001, debug=True)
