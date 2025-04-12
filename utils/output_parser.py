def format_explanation_to_text(explanation: dict) -> str:
    summary = explanation["summary"]
    keywords = explanation["keywords"]

    keyword_lines = "\n".join(f"- {kw}" for kw in keywords)

    return f"**Summary**\n- {summary}\n\n**Keywords**\n{keyword_lines}"