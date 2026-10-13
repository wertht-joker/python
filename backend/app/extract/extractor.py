"""实体抽取：简历文本 → 技能 / 学校 / 公司 / 学历 / 证书 / 项目数

采用「词典 + 规则」匹配（确定性、可解释、零幻觉），不做 LLM 抽取。
"""
import re

from app.extract import dicts
from app.kg import seed_data


def _normalize(text: str) -> str:
    """把简历里的技能别名统一替换成标准名，提升命中率"""
    for alias, std in sorted(dicts.SKILL_ALIASES.items(), key=lambda x: -len(x[0])):
        text = re.sub(re.escape(alias), std, text)
    return text


def _match_skill(text: str, skill: str) -> bool:
    """技能匹配：含英文字母用字母边界（避免 Java 误命中 JavaScript），纯中文直接包含"""
    if any(c.isascii() and c.isalpha() for c in skill):
        pattern = r"(?<![A-Za-z])" + re.escape(skill) + r"(?![A-Za-z])"
        return re.search(pattern, text, re.IGNORECASE) is not None
    return skill in text


def extract_skills(text: str) -> list[str]:
    """抽取命中的技能（归一化标准名）"""
    found = {s for s in seed_data.SKILLS if _match_skill(text, s)}
    # 消歧：命中 C++ 时去掉误命中的 C
    if "C++" in found:
        found.discard("C")
    # 命中 Spring Boot / Spring Cloud 时保留，命中 Spring 也保留（Spring 单独合法）
    return sorted(found, key=lambda s: list(seed_data.SKILLS).index(s))


def extract_school(text: str) -> str | None:
    """抽取学校（简历通常一所，取第一个命中）"""
    for school in seed_data.SCHOOLS:
        if school in text:
            return school
    # fallback：识别「XX大学/学院」但不在重点名单（双非/普通院校）
    m = re.search(r"[一-龥]{2,12}(?:大学|学院)", text)
    return m.group(0) if m else None


def extract_companies(text: str) -> list[str]:
    """抽取公司（实习/工作经历中出现的公司）"""
    return [c for c in seed_data.COMPANIES if c in text]


def extract_education(text: str) -> str | None:
    """抽取最高学历（按优先级）"""
    for keyword, level in dicts.EDUCATION_LEVELS:
        if keyword in text:
            return level
    return None


# 证书同义组：命中组内任意一个都归一成第一个（标准名），避免「英语四级（CET-4）」算两遍
CERT_SYNONYMS = [
    ("英语四级", "大学英语四级", "CET-4", "CET4"),
    ("英语六级", "大学英语六级", "CET-6", "CET6"),
]
_CERT_GROUP_MEMBERS = {s for group in CERT_SYNONYMS for s in group}


def extract_certificates(text: str) -> list[str]:
    """抽取证书（同义去重）"""
    found = []
    for synonyms in CERT_SYNONYMS:
        if any(s in text for s in synonyms):
            found.append(synonyms[0])
    for c in seed_data.CERTIFICATES:
        if c in _CERT_GROUP_MEMBERS:
            continue
        if c in text:
            found.append(c)
    return found


def _estimate_projects(text: str) -> int:
    """粗估项目数量（统计「项目」关键词出现次数，生产可换 LLM 精确解析）"""
    raw = text.count("项目")
    return max(0, min(raw, 8))


def extract(text: str) -> dict:
    """完整抽取，返回结构化实体"""
    text = _normalize(text)
    school = extract_school(text)
    # 识别到了学校但不在重点名单 → 归普通本科
    tier = seed_data.SCHOOLS.get(school) if school else None
    if school and tier is None:
        tier = "普通本科"
    return {
        "skills": extract_skills(text),
        "school": school,
        "school_tier": tier,
        "education": extract_education(text),
        "companies": extract_companies(text),
        "certificates": extract_certificates(text),
        "project_count": _estimate_projects(text),
        "has_internship": ("实习" in text) or ("工作经历" in text),
    }
