import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)


def generate_summary(stats: dict):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    client = Groq(api_key=api_key)

    prompt = f"""
You are a senior sales analyst preparing a report for executives.

Using the following statistics extracted from a sales dataset,
write a professional 3-paragraph business summary.

Sales statistics:
{stats}

Paragraph structure:
1. Overall sales performance
2. Top products or regions
3. Trends and recommendation

Maximum 200 words.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content