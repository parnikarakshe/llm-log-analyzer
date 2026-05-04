from google import genai
import json
import time

from config import GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_chunk(log_chunk):
    log_text = "".join(log_chunk)

    prompt = f"""
    You are a log analysis agent. Analyze the following logs.
    Return ONLY valid JSON. No extra text, no markdown, no backticks.

    For every ERROR, WARNING or CRITICAL line found return this structure:
    {{
        "issues": [
            {{
                "severity": "ERROR or WARNING or CRITICAL",
                "timestamp": "copy timestamp from log",
                "description": "what went wrong in simple words",
                "root_cause": "why this likely happened",
                "suggested_fix": "what should be done to fix it",
                "bug_title": "one short line describing the bug"
            }}
        ],
        "summary": "one sentence about overall health of these logs"
    }}

    Logs to analyze:
    {log_text}
    """

    # Try up to 3 times if Gemini fails
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"           Calling Gemini (attempt {attempt+1})...")
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            raw = response.text
            clean = raw.strip().replace("```json", "").replace("```", "").strip()
            result = json.loads(clean)
            return result

        except json.JSONDecodeError:
            # Gemini returned something that isn't valid JSON
            print(f"           Gemini returned invalid JSON on attempt {attempt+1}")
            time.sleep(2)

        except Exception as e:
            # Any other error like network issue
            print(f"           Error on attempt {attempt+1}: {e}")
            time.sleep(2)

    # If all 3 attempts fail, return a safe empty result
    # This means the program keeps running instead of crashing
    print("           All retries failed. Skipping this chunk.")
    return {
        "issues": [],
        "summary": "Analysis failed after 3 retries"
    }