def show_dashboard():

    total = 0
    high = 0
    medium = 0
    low = 0

    try:
        with open("logs.txt", "r") as file:
            lines = file.readlines()

        for line in lines:

            if line.startswith("Input:"):
                total += 1

            if "Severity: High" in line:
                high += 1

            elif "Severity: Medium" in line:
                medium += 1

            elif "Severity: Low" in line:
                low += 1

    except FileNotFoundError:
        print("logs.txt not found.")
        return

    print("\n==============================")
    print("        XSS DETECTOR")
    print("==============================")

    print("Total XSS detections:", total)
    print("High severity:", high)
    print("Medium severity:", medium)
    print("Low severity:", low)

    print("==============================")
    print("        Recent Logs")
    print("==============================")

    try:
        with open("logs.txt", "r") as file:
            print(file.read())

    except FileNotFoundError:
        print("No logs available.")


show_dashboard()