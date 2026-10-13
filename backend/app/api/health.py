"""健康检查"""
from fastapi import APIRouter

from app.core.config import settings
from app.kg import client

router = APIRouter(tags=["健康检查"])


@router.get("/health")
def health():
    return {
        "code": 200,
        "message": "ok",
        "data": {
            "app": "简历打分助手",
            "neo4j": client.ping(),
            "deepseek_configured": bool(settings.deepseek_api_key),
        },
    }
