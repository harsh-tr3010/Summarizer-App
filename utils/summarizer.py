import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def limit_words(text, max_words=500):
    words = text.split()
    return " ".join(words[:max_words]).strip()


def clean_output(text):
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def generate_summary(text):
    prompt = f"""
You are an expert summarizer.

Read the document carefully and create TWO summaries.

STRICT RULES:
1. English Summary must be NO MORE THAN 500 WORDS.
2. Hindi Summary must be NO MORE THAN 500 WORDS.
3. Keep both summaries concise and focused.
4. Include only key points.
5. No introductions, no explanations, no filler text.

Return EXACTLY in this format:

### English Summary
<summary>

### Hindi Summary
<summary>

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

    # Hard enforce limits separately
    english = limit_words(english, 500)
    hindi = limit_words(hindi, 500)

    return english, hindi