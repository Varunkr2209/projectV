#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS  # Optional, useful for browser access

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains (remove if unnecessary)

# Keyword mappings
FUNCTION_KEYWORDS = {
    "paid media": ("Marketing", "Performance Marketing"),
    "growth": ("Marketing", "Growth"),
    "brand": ("Marketing", "Brand Management"),
    "account executive": ("Sales", "Account Management"),
}

SENIORITY_KEYWORDS = {
    "intern": "Entry",
    "junior": "Entry",
    "associate": "Entry",
    "manager": "Manager",
    "director": "Director",
    "vp": "VP",
    "chief": "C-Level",
    "cmo": "C-Level",
    "head": "Director",
    "lead": "Manager",
    "sr": "Senior",
    "senior": "Senior"
}

@app.route('/categorise', methods=['POST'])
def categorise_job_title():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()
    title = data.get('title', '')
    if not title.strip():
        return jsonify({"error": "Missing 'title' field or empty title"}), 400

    title_lower = title.lower()
    function = sub_function = seniority = None

    # Match function & sub-function
    for keyword, (func, subfunc) in FUNCTION_KEYWORDS.items():
        if keyword.lower() in title_lower:
            function = func
            sub_function = subfunc
            break

    # Match seniority
    for keyword, level in SENIORITY_KEYWORDS.items():
        if keyword.lower() in title_lower:
            seniority = level
            break

    matched = all([function, sub_function, seniority])
    result = {
        "function": function,
        "sub_function": sub_function,
        "seniority": seniority,
        "matched": matched
    }

    return jsonify(result)

@app.route('/')
def index():
    return "Job Categorization API. Use POST /categorise with a job title in JSON format."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
