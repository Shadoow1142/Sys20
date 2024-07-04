from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    text = request.form["text"]
    keywords = request.form["keywords"].split("\n")
    keywords = [keyword.strip() for keyword in keywords if keyword.strip()]
    action = request.form["action"]

    print(f"Action: {action}")
    if action == "search":
        result = search_lines(text, keywords)
    elif action == "remove":
        result = remove_lines(text, keywords)
    elif action == "juno":
        result = extract_ids_and_ips(text)

    print(f"Result: {result}")
    return jsonify({"result": result})

def search_lines(text, keywords):
    lines = text.split("\n")
    result = [line for line in lines if any(keyword in line for keyword in keywords)]
    return result

def remove_lines(text, keywords):
    lines = text.split("\n")
    result = [line for line in lines if not any(keyword in line for keyword in keywords)]
    return result

def extract_ids_and_ips(text):
    pattern = re.compile(r".*\s(\w+)\s\[(\d+\.\d+\.\d+\.\d+)\]")
    matches = pattern.findall(text)
    result = [f"{match[0]} {match[1]}" for match in matches]
    print(f"Extracted IDs and IPs: {result}")
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
