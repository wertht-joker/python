"""图谱约束：为各节点类型的 name 建唯一索引，保证 MERGE 幂等"""
from neo4j import GraphDatabase

from app.core.config import settings

_CONSTRAINTS = [
    "CREATE CONSTRAINT job_name IF NOT EXISTS FOR (n:Job) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (n:Skill) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT school_name IF NOT EXISTS FOR (n:School) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT company_name IF NOT EXISTS FOR (n:Company) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT cert_name IF NOT EXISTS FOR (n:Certificate) REQUIRE n.name IS UNIQUE",
]


def create_constraints():
    """建约束（启动时调用，IF NOT EXISTS 保证幂等）"""
    driver = GraphDatabase.driver(settings.neo4j_uri, auth=None)
    with driver.session() as session:
        for q in _CONSTRAINTS:
            session.run(q)
    driver.close()
