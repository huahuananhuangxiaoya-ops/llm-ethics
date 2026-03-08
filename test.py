import sys
import requests

sys.stdout.reconfigure(line_buffering=True)


def main():
    payload = {
        "system_prompt": "You are a moral philosopher. Be concise.",
        "user_prompt": "Is lying ever morally acceptable? Answer in one sentence.",
    }

    def call_and_print(label: str, path: str):
        url = f"http://localhost:5000{path}"
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        print(label, flush=True)
        print("  Text :", data.get("text"), flush=True)
        print("  Error:", data.get("error"), flush=True)
        print(flush=True)

    call_and_print("Gemini:", "/api/gemini")
    call_and_print("LLaMA (Groq):", "/api/llama")
    call_and_print("DeepSeek:", "/api/deepseek")


if __name__ == "__main__":
    main()

