"""岗位技能关系图（供前端可视化）"""
from fastapi import APIRouter

from app.kg import client

router = APIRouter(tags=["知识图谱"])


@router.get("/graph/{job}")
def job_graph(job: str):
    records = client.run(
        "MATCH (j:Job {name: $job})-[r:REQUIRES]->(s:Skill) "
        "RETURN j.name AS job, s.name AS skill, r.weight AS weight",
        job=job,
    )
    if not records:
        return {"code": 404, "message": f"岗位不存在: {job}", "data": None}

    nodes = [{"name": job, "type": "job"}]
    edges = []
    for r in records:
        nodes.append({"name": r["skill"], "type": "skill", "weight": r["weight"]})
        edges.append({"from": job, "to": r["skill"], "weight": r["weight"]})

    # 去重
    seen = set()
    unique_nodes = []
    for n in nodes:
        if n["name"] not in seen:
            seen.add(n["name"])
            unique_nodes.append(n)

    return {"code": 200, "message": "ok", "data": {"nodes": unique_nodes, "edges": edges}}
