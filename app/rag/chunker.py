import re


def chunk_markdown(document):

    content = document["content"]

    parts = re.split(
        r"(?=^#{1,3}\s)",
        content,
        flags=re.MULTILINE,
    )

    chunks = []

    for part in parts:

        part = part.strip()

        if not part:
            continue

        chunks.append({
            "text": part,
            "source": document["filename"]
        })

    return chunks


def create_chunks(documents):

    all_chunks = []

    for document in documents:

        all_chunks.extend(
            chunk_markdown(document)
        )

    return all_chunks