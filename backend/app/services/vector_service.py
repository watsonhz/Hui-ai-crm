import os
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.knowledge import Knowledge

try:
    from openai import OpenAI
    from pgvector.sqlalchemy import Vector
    HAS_VECTOR = True
except ImportError:
    HAS_VECTOR = False

EMBEDDING_DIM = 1536
EMBEDDING_MODEL = "text-embedding-3-small"


def _get_client():
    api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("EMBEDDING_BASE_URL", "https://api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url) if api_key else None


def generate_embedding(text: str) -> list[float]:
    client = _get_client()
    if not client:
        # 离线模式：返回零向量
        return [0.0] * EMBEDDING_DIM
    try:
        resp = client.embeddings.create(model=EMBEDDING_MODEL, input=text[:8000])
        return resp.data[0].embedding
    except Exception:
        return [0.0] * EMBEDDING_DIM


def index_document(db: Session, knowledge_id: int):
    doc = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not doc or not doc.content:
        return
    text = f"{doc.title} {doc.content}"
    vec = generate_embedding(text)
    doc.embedding = vec
    db.commit()


def search_similar(db: Session, query: str, top_k: int = 5, category: str = None) -> list[dict]:
    vec = generate_embedding(query)
    vec_str = "[" + ",".join(str(v) for v in vec) + "]"
    sql = "SELECT id, title, content, category, 1 - (embedding <=> :vec) AS similarity FROM knowledge WHERE embedding IS NOT NULL"
    params = {"vec": vec_str, "limit": top_k}
    if category:
        sql += " AND category = :category"
        params["category"] = category
    sql += " ORDER BY embedding <=> :vec LIMIT :limit"
    rows = db.execute(text(sql), params).fetchall()
    return [{"id": r[0], "title": r[1], "content": r[2][:500],
             "category": r[3], "similarity": round(r[4], 4)} for r in rows]
