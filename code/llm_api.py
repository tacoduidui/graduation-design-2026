from config import *
import requests
import json
from zai import ZhipuAiClient

def call_glm(prompt: str) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt.strip()[:300]}
            ],
            "stream": False,
            "temperature": 0.05
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(data), timeout=15)

        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip().lower()

        if "yes" in answer:
            return "yes"
        else:
            return "no"

    except Exception as e:
        print(f"API 调用失败: {e}")
        return "no"

