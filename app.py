from flask import Flask, render_template, request, send_file, redirect
from detector import detect_xss
from scanner import analyze_reflection
from urllib.parse import urlparse

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    pattern = None
    severity = None
    user_input = ""

    if request.method == "POST":

        user_input = request.form["user_input"]

        detected, pattern, severity = detect_xss(user_input)

        if detected:

            result = "Possible XSS Detected!"

            with open("logs.txt", "a") as file:
                file.write(f"Input: {user_input}\n")
                file.write("Status: XSS Detected\n")
                file.write(f"Pattern: {pattern}\n")
                file.write(f"Severity: {severity}\n")
                file.write("-" * 30 + "\n")

        else:

            result = "No suspicious XSS pattern detected."

    return render_template(
        "index.html",
        result=result,
        pattern=pattern,
        severity=severity,
        user_input=user_input
    )


@app.route("/scan", methods=["GET", "POST"])
def scan():

    scan_result = None

    url = ""
    parameter = ""

    if request.method == "POST":

        url = request.form["url"].strip()
        parameter = request.form["parameter"].strip()

        if not url or not parameter:

              scan_result = {
                "reflected": False,
                "context": "Invalid input",
                "severity": "None",
                "message": "Please enter a URL and parameter.",
                "snippet": ""
            }


        else:

            parsed_url = urlparse(url)

            if parsed_url.scheme not in ["http", "https"]:
                scan_result = {
                   "reflected": False,
                    "context": "Invalid URL",
                    "severity": "None",
                    "message": "Please enter a valid HTTP or HTTPS URL.",
                    "snippet": ""
                }

            else:

                scan_result = analyze_reflection(
                    url,
                    parameter
                )

    return render_template(
        "scanner.html",
        result=scan_result,
        url=url,
        parameter=parameter
    )

@app.route("/dashboard")
def dashboard():

    total = 0
    high = 0
    medium = 0
    low = 0

    logs = []

    try:

        with open("logs.txt", "r") as file:
            lines = file.readlines()

        current_input = ""
        current_pattern = ""
        current_severity = ""

        for line in lines:

            line = line.strip()

            if line.startswith("Input:"):

                current_input = line.replace("Input:", "", 1).strip()

                total += 1

            elif line.startswith("Pattern:"):

                current_pattern = line.replace("Pattern:", "", 1).strip()

            elif line.startswith("Severity:"):

                current_severity = line.replace("Severity:", "", 1).strip()

                if current_severity == "High":
                    high += 1

                elif current_severity == "Medium":
                    medium += 1

                elif current_severity == "Low":
                    low += 1

            elif line.startswith("-" * 30):

                logs.append({
                    "input": current_input,
                    "pattern": current_pattern,
                    "severity": current_severity
                })

                current_input = ""
                current_pattern = ""
                current_severity = ""

    except FileNotFoundError:

        logs = []


    return render_template(
        "dashboard.html",
        total=total,
        high=high,
        medium=medium,
        low=low,
        logs=logs
    )

@app.route("/learn")
def learn():
    return render_template("learn.html")


@app.route("/report")
def report_page():

    total = 0
    high = 0
    medium = 0
    low = 0
    logs = []

    try:
        with open("logs.txt", "r") as file:
            lines = file.readlines()

        current_input = ""
        current_pattern = ""
        current_severity = ""

        for line in lines:
            line = line.strip()

            if line.startswith("Input:"):
                current_input = line.replace("Input:", "", 1).strip()
                total += 1

            elif line.startswith("Pattern:"):
                current_pattern = line.replace("Pattern:", "", 1).strip()

            elif line.startswith("Severity:"):
                current_severity = line.replace("Severity:", "", 1).strip()
                if current_severity == "High":
                    high += 1
                elif current_severity == "Medium":
                    medium += 1
                elif current_severity == "Low":
                    low += 1

            elif line.startswith("-" * 30):
                logs.append({
                    "input": current_input,
                    "pattern": current_pattern,
                    "severity": current_severity
                })
                current_input = ""
                current_pattern = ""
                current_severity = ""

    except FileNotFoundError:
        logs = []

    return render_template(
        "report.html",
        total=total,
        high=high,
        medium=medium,
        low=low,
        logs=logs
    )


@app.route("/download-ppt")
def download_ppt():
    return send_file("XSS_Guard_Academic_Project_Presentation.pptx", as_attachment=True, download_name="XSS_Guard_Academic_Project_Presentation.pptx")


@app.route("/slides")
def slides_redirect():
    return redirect("/")


@app.errorhandler(404)
def not_found(e):
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)