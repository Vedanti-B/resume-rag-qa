import re

def split_resume_sections(text):
    headers = [
        "Career Objective", "Education", "Technical Strengths",
        "Projects", "Certifications", "Strengths",
        "Hobbies", "Personal Profile"
    ]

    pattern = r"(?i)(" + "|".join(headers) + r")"
    splits = re.split(pattern, text)

    chunks = []

    # HEADER chunk (name, email, phone)
    header_chunk = splits[0].strip()
    if len(header_chunk) > 20:
        chunks.append("HEADER\n" + header_chunk)

    buffer = ""
    current_header = ""

    for part in splits[1:]:
        part = part.strip()

        if part.lower() in [h.lower() for h in headers]:
            if buffer:
                chunks.append(current_header + "\n" + buffer.strip())
            current_header = part
            buffer = ""
        else:
            buffer += " " + part

    if buffer:
        chunks.append(current_header + "\n" + buffer.strip())

    return chunks
