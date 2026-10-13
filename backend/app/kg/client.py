"""Neo4j 连接与通用查询封装"""
from neo4j import GraphDatabase

from app.core.config import settings

_driver = None


def get_driver():
    """惰性创建全局驱动（线程安全）"""
    global _driver
    if _driver is None:
        # docker-compose 里 NEO4J_AUTH=none，本地免密连接
        _driver = GraphDatabase.driver(settings.neo4j_uri, auth=None)
    return _driver


def run(query: str, **params) -> list:
    """执行查询，返回结果记录列表"""
    driver = get_driver()
    with driver.session() as session:
        return list(session.run(query, **params))


def run_single(query: str, **params):
    """执行查询，返回第一条记录（无则 None）"""
    result = run(query, **params)
    return result[0] if result else None


def ping() -> bool:
    """检查 Neo4j 是否可连接"""
    try:
        run_single("RETURN 1 AS ok")
        return True
    except Exception:
        return False
