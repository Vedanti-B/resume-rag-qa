import re

def extract_personal_info(text):
    info = {}

    first_line = text.strip().split("\n")[0]
    if len(first_line.split()) >= 2:
        info["name"] = first_line.strip()

    email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    info["email"] = email.group() if email else "Not mentioned"

    phone = re.search(r"\+?\d{10,13}", text.replace(" ", ""))
    info["phone"] = phone.group() if phone else "Not mentioned"

    return info
