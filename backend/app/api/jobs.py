"""岗位列表"""
from fastapi import APIRouter

from app.kg import client

router = APIRouter(tags=["岗位"])


@router.get("/jobs")
def list_jobs():
    records = client.run(
        "MATCH (j:Job) RETURN j.name AS name, j.category AS category ORDER BY j.name"
    )
    data = [{"name": r["name"], "category": r["category"]} for r in records]
    return {"code": 200, "message": "ok", "data": data}
