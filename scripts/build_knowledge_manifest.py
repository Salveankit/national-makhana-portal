from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.knowledge import knowledge_base_summary, load_knowledge_documents


def main() -> None:
    root = Path("knowledge")
    root.mkdir(parents=True, exist_ok=True)
    manifest = knowledge_base_summary()
    manifest["documents_detail"] = [
        {
            "doc_id": document.doc_id,
            "title": document.title,
            "category": document.category,
            "summary": document.summary,
            "source_type": document.source_type,
            "path": document.path,
            "tags": document.tags,
        }
        for document in load_knowledge_documents()
    ]
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
