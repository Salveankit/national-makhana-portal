import unittest

from backend.app.knowledge import knowledge_base_summary, load_knowledge_chunks, load_knowledge_documents


class KnowledgeBaseTests(unittest.TestCase):
    def test_knowledge_documents_load(self):
        documents = load_knowledge_documents()
        self.assertGreaterEqual(len(documents), 4)
        self.assertTrue(any(doc.category == "official" for doc in documents))
        self.assertTrue(any(doc.category == "faq" for doc in documents))

    def test_knowledge_chunks_are_generated(self):
        chunks = load_knowledge_chunks()
        self.assertGreater(len(chunks), 0)
        self.assertTrue(all(chunk.text for chunk in chunks))

    def test_knowledge_summary_reports_categories(self):
        summary = knowledge_base_summary()
        self.assertIn("official", summary["categories"])
        self.assertIn("faq", summary["categories"])
        self.assertEqual(summary["provider"], "azure_openai")
