from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    tokenizer="google/flan-t5-base"
)

def retrieve_context(question, chunks, embedder, index, top_k=4):
    q_emb = embedder.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(q_emb, top_k)
    context = []

    for score, idx in zip(scores[0], indices[0]):
        if score > 0.35:
            chunk = chunks[idx]

            if "name" in question.lower() and "HEADER" in chunk:
                context.append(chunk)
            elif "project" in question.lower() and "Projects" in chunk:
                context.append(chunk)
            elif "certification" in question.lower() and "Certifications" in chunk:
                context.append(chunk)
            elif "career objective" in question.lower() and "Career Objective" in chunk:
                context.append(chunk)
            elif "language" in question.lower() and "Technical Strengths" in chunk:
                context.append(chunk)
            elif len(context) == 0:
                context.append(chunk)

    return "\n\n".join(context[:2])


def ask_question(question, personal_info, chunks, embedder, index):
    q_lower = question.lower()

    if "name" in q_lower:
        return personal_info.get("name", "Not mentioned")
    if "email" in q_lower:
        return personal_info.get("email", "Not mentioned")
    if "phone" in q_lower:
        return personal_info.get("phone", "Not mentioned")

    context = retrieve_context(question, chunks, embedder, index)

    prompt = f"""
You are an ATS resume assistant.
Answer only from the resume section below.
If not found, say "Not mentioned in resume".

Resume:
{context}

Question:
{question}

Answer:
"""

    return generator(
        prompt,
        max_new_tokens=120,
        do_sample=False
    )[0]["generated_text"]
