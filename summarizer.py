import os
import openai

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
        if provider == "grok":
            openai.api_key = os.getenv("GROK_API_KEY")
            openai.api_base = "https://api.x.ai/v1"
            model = "grok-beta"
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            openai.api_base = "https://api.openai.com/v1"
            model = "gpt-4"

        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.3,
        )

        content = response.choices[0].message.content.strip()
        print(f"🤖 {provider.upper()} Response: {content}")

        summary = ""
        impact = "Neutral"
        for line in content.splitlines():
            if line.lower().startswith("summary"):
                summary = line.split(":", 1)[1].strip()
            elif line.lower().startswith("impact"):
                impact = line.split(":", 1)[1].strip().capitalize()

        return summary, impact

    except Exception as e:
        print(f"❌ {provider.upper()} summarization failed: {e}")
        return f"{provider.upper()} AI failed", "Neutral"
