from flask import Flask, render_template, request
import google.generativeai as genai
import os

app = Flask(__name__)

# Set your Gemini API Key here
genai.configure(api_key="AIzaSyC2-xYC7mrE-Qa4BMBFIU-2gLrVCId2hAU")

# Stateless generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 40,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel("models/gemini-2.0-flash")


def generate_prompt(short_desc, location, req, resp):
    prompt = f"""
You are a security expert. Generate a vulnerability report based on the following input.

Description of vulnerability:
{short_desc}

Location of vulnerability:
{location}

Request (optional):
{req if req else "Not provided"}

Response (optional):
{resp if resp else "Not provided"}

Return a structured response in this format:
1. Descriptive title of the vulnerability
2. Description of the vulnerability (first explain what the vulnerability is and how it can be exploited , then explain the location and exploitation in this scenario using the context and request if provided , and finally explain what an attacker can achieve by exploiting this vulnerability in this scenario (around 3 lines) — in 3 paragraphs)
3. Mitigation steps (at least 3)
4. Severity (Low / Medium / High / Critical)

Respond clearly in text for rendering on a webpage.
"""
    return prompt


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        short_desc = request.form.get("short_desc")
        location = request.form.get("location")
        req = request.form.get("req")
        resp = request.form.get("resp")

        prompt = generate_prompt(short_desc, location, req, resp)

        # Stateless content generation
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            stream=False  # Disable streaming to avoid memory state
        )
        result = response.text
       # print(result)
    return render_template("index.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)
