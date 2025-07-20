import os
import google.generativeai as genai

# Load Gemini API key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a supported model (e.g., gemini-1.5-pro or gemini-2.0-flash)
model = genai.GenerativeModel("gemini-2.0-flash")  # Updated model name

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
        # Generate content using the model
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

# Example usage
if __name__ == "__main__":
    title = "OPEC Announces Increase in Oil Production Quotas"
    description = "OPEC countries have agreed to increase oil production by 500,000 barrels per day starting next month."
    summary, impact = analyze_news(title, description)
    print(f"Summary: {summary}")
    print(f"Impact: {impact}")
