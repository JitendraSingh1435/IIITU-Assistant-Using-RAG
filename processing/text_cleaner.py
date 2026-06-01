def clean_text(text_input):
    if isinstance(text_input, str):
        text_items = [text_input]
    else:
        text_items = text_input or []

    cleaned = []

    for item in text_items:
        text = str(item).strip()
        if len(text) > 3:
            cleaned.append(text)

    return " ".join(cleaned)
