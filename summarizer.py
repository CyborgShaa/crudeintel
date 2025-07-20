import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_news(title, description=None):
    prompt = f"""
You are a market analyst. Read this headline and summarize it in one line. Then classify its market impact on crude oil as Bullish, Bearish, or Neutral.

Title: "{title}"
Description: "{description or 'N/A'}"

Respond in the format:
Summary: <one-line summary>
Impact: <Bullish/Bearish/Neutral>
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.4,
        )

        # ✅ Debug print statements
        print("🔁 GPT Prompt Sent")
        print("🔁 GPT Response:", response.choices[0].message.content.strip())

        content = response.choices[0].message.content.strip()
        summary_line = ""
        impact_tag = "Neutral"

        for line in content.splitlines():
            if line.lower().startswith("summary"):
                summary_line = line.split(":", 1)[1].strip()
            elif line.lower().startswith("impact"):
                impact_tag = line.split(":", 1)[1].strip().capitalize()

        return summary_line, impact_tag

    except Exception as e:
        print(f"❌ AI summarization failed: {e}")
        return None, "Neutral"
