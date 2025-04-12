from typing import Dict, List

EXPLAIN_PROMPT = """
You are an expert assistant who helps users understand technical IT concepts in simple language.

Given the following text, do the following two tasks:

1. Identify the important technical terms (keywords) that **appear directly in the input text**.
   - Only extract words that are **literally present in the given text**. Do not include inferred or related terms that are not in the text.

2. For each keyword, include a brief explanation in the same string using this format:
   - `"keyword: short explanation"`
   - Example: `"string: a sequence of characters used to represent text"`

3. Provide a beginner-friendly summary of the overall meaning of the text.

Return your response strictly in the following JSON format:
{{
  "keywords": [
    "keyword1: short explanation",
    "keyword2: short explanation"
  ],
  "summary": "Beginner-friendly summary."
}}

Now, analyze this text:

Term: {text}

Return only a valid JSON response.
"""

def get_explain_prompt(text: str) -> str:
    return EXPLAIN_PROMPT.format(text=text)