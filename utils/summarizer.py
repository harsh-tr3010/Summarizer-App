import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def word_count(text):
    return len(text.split())


def limit_words(text, max_words=500):
    words = text.split()
    return " ".join(words[:max_words]).strip()


def clean_output(text):
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def pad_if_too_short(text, minimum=300):
    """
    If model returns too short content, keep as-is.
    We guide the model strongly in prompt, so this is mainly fallback.
    """
    return text.strip()


def generate_summary(text):
    prompt = f"""
You are an expert analyst and summarizer.

Read the document VERY CAREFULLY and understand the complete context before writing.

Create TWO summaries:
1. English Summary
2. Hindi Summary

STRICT RULES:
- Each summary should be between 300 and 500 words.
- Never exceed 500 words.
- Include all major points, insights, findings, conclusions, and relevant details.
- Be concise but informative.
- Do not make it too short.
- Do not repeat points.
- Use clear professional language.
- Preserve factual meaning.

Return EXACTLY in this format:

### English Summary
<300 to 500 words summary>

### Hindi Summary
<300 to 500 words summary>

Document:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    output = clean_output(response.choices[0].message.content)

    english = ""
    hindi = ""

    if "### Hindi Summary" in output:
        parts = output.split("### Hindi Summary", 1)
        english = parts[0].replace("### English Summary", "").strip()
        hindi = parts[1].strip()
    else:
        english = output.strip()
        hindi = "Hindi summary could not be generated."

    english = pad_if_too_short(english, 300)
    hindi = pad_if_too_short(hindi, 300)

    
    english = limit_words(english, 500)
    hindi = limit_words(hindi, 500)

    return english, hindi