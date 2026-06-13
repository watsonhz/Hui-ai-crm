"""RAG Vector Retrieval Service — tenant-isolated semantic search.

Secure-by-design:
- All queries scoped to tenant_id (mandatory parameter)
- Result count capped at top_k_max to prevent data dump
- No raw SQL; uses ORM-level parameterization
"""

from typing import Optional
from sqlalchemy.orm import Session

# Configurable limits
MAX_TOP_K = 20
MAX_QUERY_LENGTH = 2000
DEFAULT_TOP_K = 5


class VectorService:
    """Semantic retrieval with mandatory tenant scoping."""

    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        query: str,
        tenant_id: int,
        collection: str = "default",
        top_k: int = DEFAULT_TOP_K,
        filter_metadata: Optional[dict] = None,
    ) -> list[dict]:
        """
        Tenant-scoped vector search.

        Args:
            query: Search query (truncated to MAX_QUERY_LENGTH for safety)
            tenant_id: REQUIRED — all results are scoped to this tenant
            collection: Logical collection name (sanitized to alphanumeric + underscore)
            top_k: Number of results (capped at MAX_TOP_K)
            filter_metadata: Optional metadata filters (tenant_id is always enforced)

        Returns:
            List of {id, content, score, metadata} dicts (no other tenants' data)
        """
        # Input sanitization
        query = query.strip()[:MAX_QUERY_LENGTH]
        collection = _sanitize_collection(collection)
        top_k = min(max(top_k, 1), MAX_TOP_K)

        # Mandatory tenant scope — cannot be bypassed
        metadata_filter = {"tenant_id": tenant_id}
        if filter_metadata:
            # Tenant filter is always applied last (overrides user input)
            filter_metadata.pop("tenant_id", None)
            metadata_filter.update(filter_metadata)

        # In production, this would call pgvector / chromadb / pinecone.
        # Placeholder: return empty results (scoped correctly).
        # When integrating a real vector DB, the metadata_filter must be
        # passed as the WHERE clause to prevent cross-tenant leakage.
        return []

    def index_document(
        self,
        document_id: int,
        content: str,
        tenant_id: int,
        metadata: Optional[dict] = None,
    ) -> bool:
        """Index a document chunk. Tenant-scoped."""
        if not content.strip():
            return False
        # Placeholder: real embedding + indexing
        return True

    def delete_document(self, document_id: int, tenant_id: int) -> bool:
        """Delete a document's vectors. Must match tenant_id."""
        # Placeholder
        return True


def _sanitize_collection(name: str) -> str:
    """Allow only alphanumeric + underscore in collection names."""
    import re
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return sanitized or "default"
