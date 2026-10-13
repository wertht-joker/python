"""FastAPI 主入口"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import grade, graph, health, jobs, upload
from app.core.config import settings
from app.kg import schema, seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动时初始化知识图谱（建约束 + 幂等导入预置数据）"""
    try:
        schema.create_constraints()
        seed.seed()
        print("知识图谱已就绪（约束 + 预置数据导入完成）")
    except Exception as e:
        print(f"[警告] Neo4j 初始化失败，请先启动 Docker 并 `docker compose up -d`：{e}")
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="基于知识图谱的简历打分助手（实体抽取 + 图谱匹配 + LLM 建议）",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (health.router, jobs.router, upload.router, grade.router, graph.router):
    app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["根路由"])
def root():
    return {"app": settings.app_name, "docs": "/docs", "health": "/api/v1/health"}
