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
4. When generating a response, please match the language of the input text.
   - If the input is in English, respond in English.
   - If it is in Korean, respond in Korean.
   - If it is in British English, respond in British English accordingly.

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

ADDITIONAL_EXPLAIN_PROMPT = """
You are a helpful assistant who specializes in making technical concepts easy for beginners to understand.

The user originally asked this question:
"{text}"

You previously gave them this explanation:
{result}

But the user still finds it difficult to understand.

So your task is to rewrite the explanation in a much more explain and more beginner-friendly way,  
as if you're talking to someone with **no technical background at all** — like a complete non-expert.
so you need to rewrite the explanation more example and easy to understand.

Please follow these instructions carefully:

1. Keep the **structure** exactly the same:
   - Start with `"Summary: ..."`
   - Then `"Keywords:"` followed by each keyword line starting with a dash (`-`).

2. Rephrase the **summary** so that it's very easy to understand. Use short sentences, everyday language, and no technical jargon.

3. For each **keyword**, give a clear, friendly explanation in plain language.
   - Feel free to use analogies or examples if it helps.
   - Assume the user is completely new to the term.

4. Do not remove any important information. Explain it — don’t skip it.
   - Be more helpful, not just shorter.

5. Identify the important technical text (keywords) that **appear directly in the input text**.
   - Only extract words that are **literally present in the given text**. Do not include inferred or related terms that are not in the text.

6. Detect the language of the input (`result`) and match it in your response.
   - If it’s English, answer in English.
   - If it’s Korean, answer in Korean.
   - If it’s British English, use British spelling and tone.

Return your response **strictly** in the following JSON format:
{{
  "keywords": [
    "keyword1: simple explanation",
    "keyword2: simple explanation"
  ],
  "summary": "Beginner-friendly summary."
}}

Now, rewrite the explanation based on the user's original question and the previous result.

Term: {text}

Return only the valid JSON response. Do not include any additional explanation or commentary.
"""

def get_explain_prompt(text: str) -> str:
    return EXPLAIN_PROMPT.format(text=text)

def get_additional_explain_prompt(text: str, result: str) -> str:
    return ADDITIONAL_EXPLAIN_PROMPT.format(text=text, result=result)