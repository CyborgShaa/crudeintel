import os
import google.generativeai as genai

# Load Gemini API key from secrets
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use correct model name — no "models/" prefix
model = genai.GenerativeModel("gemini-pro")

def analyze_news(title, description=None, provider="gemini"):
    prompt = f"""
You are a market analyst. Read this headline and description, then:
1. Summarize the news in one sentence.
2. Classify its impact on crude oil as Bullish, Bearish, or Neutral.

Title: "{title}"
Description: "{description or 'N/A'}"

Respond in this format:
Summary: <one-line summary>
Impact: <Bullish/Bearish/Neutral>
"""

    try:
        # ✅ Correct method for Gemini Pro
        response = model.generate_content(prompt)
        content = response.text.strip()

        summary = ""
        impact = "Neutral"
        for line in content.splitlines():
            if line.lower().startswith("summary"):
                summary = line.split(":", 1)[1].strip()
            elif line.lower().startswith("impact"):
                impact = line.split(":", 1)[1].strip().capitalize()

        return summary, impact

    except Exception as e:
        print(f"❌ Gemini summarization failed: {e}")
        return f"Gemini AI failed: {e}", "Neutral"
