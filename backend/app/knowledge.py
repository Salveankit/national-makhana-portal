from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from backend.app.core.config import settings

TEXT_FILE_SUFFIXES = {".md", ".txt"}


@dataclass(slots=True)
class KnowledgeDocument:
    doc_id: str
    title: str
    category: str
    audience: str
    source_type: str
    summary: str
    content: str
    path: str
    tags: list[str]


@dataclass(slots=True)
class KnowledgeChunk:
    chunk_id: str
    doc_id: str
    title: str
    category: str
    audience: str
    source_type: str
    summary: str
    text: str
    path: str
    tags: list[str]


def knowledge_root() -> Path:
    return Path(settings.knowledge_base_dir)


def _load_text_document(path: Path) -> KnowledgeDocument:
    content = path.read_text(encoding="utf-8").strip()
    title = path.stem.replace("-", " ").replace("_", " ").title()
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    summary_line = next((line.lstrip("# ").strip() for line in lines if line.strip("# ").strip()), title)
    summary = summary_line[:180] if summary_line else title
    category = path.parent.name
    return KnowledgeDocument(
        doc_id=path.relative_to(knowledge_root()).as_posix(),
        title=title,
        category=category,
        audience="public",
        source_type="curated_markdown",
        summary=summary,
        content=content,
        path=str(path),
        tags=[category],
    )


def _load_json_document(path: Path) -> list[KnowledgeDocument]:
    records = json.loads(path.read_text(encoding="utf-8"))
    documents: list[KnowledgeDocument] = []
    for index, record in enumerate(records):
        answer = str(record.get("answer", "")).strip()
        question = str(record.get("question", "")).strip()
        title = question or f"{path.stem} {index + 1}"
        documents.append(
            KnowledgeDocument(
                doc_id=f"{path.relative_to(knowledge_root()).as_posix()}#{index + 1}",
                title=title,
                category=path.parent.name,
                audience=str(record.get("audience", "public")),
                source_type="curated_json",
                summary=question[:180] if question else title,
                content=f"Question: {question}\nAnswer: {answer}",
                path=str(path),
                tags=list(record.get("tags", [])),
            )
        )
    return documents


def load_knowledge_documents() -> list[KnowledgeDocument]:
    root = knowledge_root()
    if not root.exists():
        return []
    documents: list[KnowledgeDocument] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.parent == root:
            continue
        if path.suffix.lower() in TEXT_FILE_SUFFIXES:
            documents.append(_load_text_document(path))
        elif path.suffix.lower() == ".json":
            documents.extend(_load_json_document(path))
    return documents


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    normalized = " ".join(text.split())
    if not normalized:
        return []
    chunks: list[str] = []
    start = 0
    step = max(chunk_size - overlap, 1)
    while start < len(normalized):
        chunk = normalized[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks


def load_knowledge_chunks() -> list[KnowledgeChunk]:
    chunks: list[KnowledgeChunk] = []
    for document in load_knowledge_documents():
        split_chunks = _split_text(document.content, settings.knowledge_chunk_size, settings.knowledge_chunk_overlap)
        for index, chunk in enumerate(split_chunks, start=1):
            chunks.append(
                KnowledgeChunk(
                    chunk_id=f"{document.doc_id}::chunk-{index}",
                    doc_id=document.doc_id,
                    title=document.title,
                    category=document.category,
                    audience=document.audience,
                    source_type=document.source_type,
                    summary=document.summary,
                    text=chunk,
                    path=document.path,
                    tags=document.tags,
                )
            )
    return chunks


def knowledge_base_summary() -> dict[str, Any]:
    documents = load_knowledge_documents()
    chunks = load_knowledge_chunks()
    categories: dict[str, int] = {}
    for document in documents:
        categories[document.category] = categories.get(document.category, 0) + 1
    return {
        "enabled": settings.chatbot_enabled,
        "provider": settings.chatbot_provider,
        "knowledge_root": str(knowledge_root()),
        "documents": len(documents),
        "chunks": len(chunks),
        "categories": categories,
        "gemini_model": settings.gemini_model,
        "gemini_configured": bool(settings.gemini_api_key),
    }
