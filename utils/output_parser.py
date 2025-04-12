def format_explanation_to_text(explanation: dict) -> str:
    summary = explanation["summary"]
    keywords = explanation["keywords"]

    keyword_lines = "\n".join(f"- {kw}" for kw in keywords)

    return f"Keywords\n{keyword_lines}\n\nSummary\n- {summary}"
