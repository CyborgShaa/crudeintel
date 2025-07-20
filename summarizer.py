import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_news(title, description=None, provider="gpt"):
    prompt = f"""
You are a market analyst. Read this headline and summarize it in one sentence. Then classify its impact on crude oil as Bullish, Bearish, or Neutral.

Title: "{title}"
Description: "{description or 'N/A'}"

Respond in format:
Summary: <your summary>
Impact: <Bullish/Bearish/Neutral>
"""

    try:
        if provider == "gpt":
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.3,
            )

            content = chat_completion.choices[0].message.content.strip()

            summary = ""
            impact = "Neutral"
            for line in content.splitlines():
                if line.lower().startswith("summary"):
                    summary = line.split(":", 1)[1].strip()
                elif line.lower().startswith("impact"):
                    impact = line.split(":", 1)[1].strip().capitalize()

            return summary, impact

        else:
            return "❌ Unsupported provider", "Neutral"

    except Exception as e:
        print(f"❌ Summarization failed: {e}")
        return f"AI failed: {e}", "Neutral"
