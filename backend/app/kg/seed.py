"""幂等导入预置图谱数据（MERGE 保证重复执行不产生重复节点）"""
from app.kg import client, seed_data


def seed():
    """把技能/学校/公司/证书/岗位/关系导入 Neo4j"""
    # 1. 技能节点
    skill_rows = [{"name": n, "category": c} for n, c in seed_data.SKILLS.items()]
    client.run(
        "UNWIND $rows AS row "
        "MERGE (s:Skill {name: row.name}) SET s.category = row.category",
        rows=skill_rows,
    )

    # 2. 学校节点
    school_rows = [{"name": n, "tier": t} for n, t in seed_data.SCHOOLS.items()]
    client.run(
        "UNWIND $rows AS row "
        "MERGE (s:School {name: row.name}) SET s.tier = row.tier",
        rows=school_rows,
    )

    # 3. 公司节点
    company_rows = [{"name": n, "tier": t} for n, t in seed_data.COMPANIES.items()]
    client.run(
        "UNWIND $rows AS row "
        "MERGE (c:Company {name: row.name}) SET c.tier = row.tier",
        rows=company_rows,
    )

    # 4. 证书节点
    cert_rows = [{"name": n, "value": v} for n, v in seed_data.CERTIFICATES.items()]
    client.run(
        "UNWIND $rows AS row "
        "MERGE (c:Certificate {name: row.name}) SET c.value = row.value",
        rows=cert_rows,
    )

    # 5. 岗位节点 + 6. 岗位→技能 关系
    for job_name, job in seed_data.JOBS.items():
        client.run(
            "MERGE (j:Job {name: $name}) SET j.category = $category, j.level = $level",
            name=job_name, category=job["category"], level=job["level"],
        )
        for weight_level, skills in job["requires"].items():
            for skill in skills:
                client.run(
                    "MATCH (j:Job {name: $job}) "
                    "MATCH (s:Skill {name: $skill}) "
                    "MERGE (j)-[r:REQUIRES]->(s) SET r.weight = $weight",
                    job=job_name, skill=skill, weight=weight_level,
                )

    # 7. 技能相关性（同义词等价）：Spring 与 Spring Boot 等
    related_pairs = [
        ("Spring", "Spring Boot"),
        ("MyBatis", "MyBatis-Plus"),
        ("Kubernetes", "Docker"),
        ("NLP", "自然语言处理"),
        ("RAG", "LangChain"),
    ]
    for a, b in related_pairs:
        client.run(
            "MATCH (x:Skill {name: $a}) MATCH (y:Skill {name: $b}) "
            "MERGE (x)-[:RELATED_TO]->(y)",
            a=a, b=b,
        )
