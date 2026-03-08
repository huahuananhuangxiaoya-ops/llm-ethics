from concurrent.futures import ThreadPoolExecutor
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
from openai import OpenAI


load_dotenv()

app = Flask(__name__)
CORS(app)


def call_gemini(system_prompt: str, user_prompt: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"text": None, "error": "GEMINI_API_KEY is not set"}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt,
        )
        response = model.generate_content(user_prompt)
        text = ""
        # google-generativeai 生成结果通常在 response.text
        if hasattr(response, "text"):
            text = response.text or ""
        else:
            text = str(response)
        return {"text": text, "error": None}
    except Exception as e:
        return {"text": None, "error": str(e)}


def call_llama(system_prompt: str, user_prompt: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"text": None, "error": "GROQ_API_KEY is not set"}

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = completion.choices[0].message.content
        return {"text": text, "error": None}
    except Exception as e:
        return {"text": None, "error": str(e)}


def call_deepseek(system_prompt: str, user_prompt: str) -> dict:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return {"text": None, "error": "DEEPSEEK_API_KEY is not set"}

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = completion.choices[0].message.content
        return {"text": text, "error": None}
    except Exception as e:
        return {"text": None, "error": str(e)}


@app.route("/api/compare", methods=["POST"])
def compare():
    data = request.get_json(silent=True) or {}
    system_prompt = data.get("system_prompt")
    user_prompt = data.get("user_prompt")

    if not system_prompt or not user_prompt:
        return (
            jsonify(
                {
                    "error": "Both 'system_prompt' and 'user_prompt' are required.",
                }
            ),
            400,
        )

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            "gemini": executor.submit(call_gemini, system_prompt, user_prompt),
            "llama": executor.submit(call_llama, system_prompt, user_prompt),
            "deepseek": executor.submit(call_deepseek, system_prompt, user_prompt),
        }

        results = {name: future.result() for name, future in futures.items()}

    return jsonify(results)


def _parse_body():
    data = request.get_json(silent=True) or {}
    system_prompt = data.get("system_prompt")
    user_prompt = data.get("user_prompt")
    if not system_prompt or not user_prompt:
        return None, None, (
            jsonify(
                {
                    "error": "Both 'system_prompt' and 'user_prompt' are required.",
                }
            ),
            400,
        )
    return system_prompt, user_prompt, None


@app.route("/api/gemini", methods=["POST"])
def api_gemini():
    system_prompt, user_prompt, error_response = _parse_body()
    if error_response is not None:
        return error_response
    result = call_gemini(system_prompt, user_prompt)
    return jsonify(result)


@app.route("/api/llama", methods=["POST"])
def api_llama():
    system_prompt, user_prompt, error_response = _parse_body()
    if error_response is not None:
        return error_response
    result = call_llama(system_prompt, user_prompt)
    return jsonify(result)


@app.route("/api/deepseek", methods=["POST"])
def api_deepseek():
    system_prompt, user_prompt, error_response = _parse_body()
    if error_response is not None:
        return error_response
    result = call_deepseek(system_prompt, user_prompt)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

