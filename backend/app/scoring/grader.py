"""分维度打分引擎（规则 + 图谱关系，可解释、非黑盒）

五个维度各 0~100，加权汇总总分：
- 技能匹配 40%：简历命中技能 / 岗位要求技能，按权重（核心/重要/加分）计
- 学历背景 20%：学校梯队 + 学历
- 项目经验 20%：项目数量 + 技术栈对岗位技能的覆盖度
- 实习经历 15%：实习公司梯队
- 证书加分  5%：证书累计加分

每个分数都能回推到「命中了哪个节点 / 缺了哪个技能」。
"""
from app.core.config import settings
from app.kg import client, seed_data

# 学校梯队分（0~50）
TIER_SCORE = {"顶尖": 50, "985": 42, "211": 34, "双一流": 32, "普通本科": 24, "专科": 14}
# 学历分（0~50）
DEGREE_SCORE = {"博士": 50, "硕士": 45, "本科": 35, "专科": 25}
# 公司梯队分（0~100）
COMPANY_SCORE = {"大厂": 100, "独角兽": 85, "中厂": 70, "小厂": 50}


def get_job_requirements(job_name: str) -> list[dict]:
    """查图谱：岗位要求的所有技能及其权重（核心/重要/加分）"""
    records = client.run(
        "MATCH (j:Job {name: $job})-[r:REQUIRES]->(s:Skill) "
        "RETURN s.name AS skill, r.weight AS weight",
        job=job_name,
    )
    return [{"skill": rec["skill"], "weight": rec["weight"]} for rec in records]


def _skill_score(matched: set[str], reqs: list[dict]) -> tuple[int, list, list]:
    """技能匹配分 + 命中/缺失明细"""
    total_w = sum(seed_data.WEIGHT_VALUE[r["weight"]] for r in reqs)
    hit = [r for r in reqs if r["skill"] in matched]
    miss = [r for r in reqs if r["skill"] not in matched]
    hit_w = sum(seed_data.WEIGHT_VALUE[r["weight"]] for r in hit)
    score = round(hit_w / total_w * 100) if total_w else 0
    return score, hit, miss


def _education_score(school_tier: str | None, education: str | None) -> int:
    s = TIER_SCORE.get(school_tier, 10) if school_tier else 10
    d = DEGREE_SCORE.get(education, 15) if education else 15
    return s + d


def _project_score(project_count: int, matched: set[str], reqs: list[dict]) -> int:
    # 项目数量分（0~50）
    if project_count <= 0:
        n = 0
    elif project_count == 1:
        n = 20
    elif project_count == 2:
        n = 35
    else:
        n = 50
    # 技术覆盖分（0~50）：命中的技能占岗位要求比例
    total = len(reqs)
    hit = sum(1 for r in reqs if r["skill"] in matched)
    c = round(hit / total * 50) if total else 0
    return n + c


def _experience_score(companies: list[str], has_internship: bool) -> int:
    if companies:
        tiers = [seed_data.COMPANIES.get(c, "小厂") for c in companies]
        return max(COMPANY_SCORE.get(t, 50) for t in tiers)
    # 有实习/工作经历但公司未进词典（多为中小厂）
    return 40 if has_internship else 0


def _certificate_score(certificates: list[str]) -> int:
    total = sum(seed_data.CERTIFICATES.get(c, 0) for c in certificates)
    return min(total, 100)


def grade(entities: dict, job_name: str) -> dict:
    """对一份简历做完整打分，返回总分 + 各维度 + 明细"""
    matched = set(entities.get("skills", []))
    reqs = get_job_requirements(job_name)

    if not reqs:
        raise ValueError(f"岗位不存在或未配置技能: {job_name}")

    skill_score, hits, miss = _skill_score(matched, reqs)
    edu_score = _education_score(entities.get("school_tier"), entities.get("education"))
    proj_score = _project_score(entities.get("project_count", 0), matched, reqs)
    exp_score = _experience_score(entities.get("companies", []), entities.get("has_internship", False))
    cert_score = _certificate_score(entities.get("certificates", []))

    dims = {
        "skill": {"name": "技能匹配", "score": skill_score, "weight": settings.w_skill},
        "education": {"name": "学历背景", "score": edu_score, "weight": settings.w_education},
        "project": {"name": "项目经验", "score": proj_score, "weight": settings.w_project},
        "experience": {"name": "实习经历", "score": exp_score, "weight": settings.w_experience},
        "certificate": {"name": "证书加分", "score": cert_score, "weight": settings.w_certificate},
    }

    total = round(sum(d["score"] * d["weight"] for d in dims.values()), 1)

    return {
        "total": total,
        "job": job_name,
        "dimensions": dims,
        "matched_skills": [r["skill"] for r in hits],
        "missing_skills": [r["skill"] for r in miss],
        "core_missing": [r["skill"] for r in miss if r["weight"] == "核心"],
    }
