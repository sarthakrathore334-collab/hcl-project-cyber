from flask import Flask, request

app = Flask(__name__)


@app.route("/search")
def search():

    query = request.args.get("q", "")

    return f"""
    <html>
        <body>
            <h1>Search Page</h1>

            <p>You searched for: {query}</p>

        </body>
    </html>
    """


@app.route("/safe")
def safe():

    query = request.args.get("q", "")

    from markupsafe import escape

    return f"""
    <html>
        <body>
            <h1>Safe Search Page</h1>

            <p>You searched for: {escape(query)}</p>

        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(port=5001, debug=True)