from pathlib import Path

# app/rag/loader.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent
KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"


def load_markdown_documents():
    documents = []

    if not KNOWLEDGE_BASE.exists():
        print(f"Knowledge base not found: {KNOWLEDGE_BASE}")
        return documents

    for file in KNOWLEDGE_BASE.glob("*.md"):
        with open(file, "r", encoding="utf-8") as f:
            documents.append({
                "filename": file.name,
                "content": f.read()
            })

    return documents