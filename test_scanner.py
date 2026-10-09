from scanner import analyze_reflection
url = "http://127.0.0.1:5001/safe"
parameter = "q"
result = analyze_reflection(url, parameter)
print("\n==============================")
print("       XSS REFLECTION SCANNER")
print("==============================")

print("Reflected:", result["reflected"])
print("Context:", result["context"])
print("Severity:", result["severity"])

if result["reflected"]:
    print("\nResponse snippet:")
    print(result["snippet"])