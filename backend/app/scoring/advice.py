"""用 DeepSeek 生成针对性改进建议（打分之外的 LLM 应用）

设计边界：打分用规则+图谱（可解释），LLM 只负责把「缺失技能 + 各维度分」
转成自然、个性化的改进建议，不参与打分本身。
"""
from openai import OpenAI

from app.core.config import settings

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )
    return _client


def generate_advice(entities: dict, grade_result: dict) -> str | None:
    """生成改进建议；未配置 API Key 时返回 None"""
    if not settings.deepseek_api_key:
        return None

    dims = grade_result["dimensions"]
    prompt = f"""你是资深 HR 和职业规划顾问。根据下面的简历分析结果，给出针对性、可执行的改进建议。

目标岗位：{grade_result['job']}
总分：{grade_result['total']} / 100
各维度得分：技能匹配 {dims['skill']['score']}，学历背景 {dims['education']['score']}，项目经验 {dims['project']['score']}，实习经历 {dims['experience']['score']}，证书加分 {dims['certificate']['score']}
已掌握技能：{'、'.join(grade_result['matched_skills']) or '（未识别到）'}
缺失技能：{'、'.join(grade_result['missing_skills']) or '无'}
核心缺失：{'、'.join(grade_result['core_missing']) or '无'}
学历：{entities.get('education') or '未知'}；学校：{entities.get('school') or '未知'}
实习/公司：{'、'.join(entities.get('companies', [])) or '无'}

请输出（控制在 200 字以内，分点）：
1. 最该补齐的 2~3 项技能，每项给一个具体可落地的学习或项目建议；
2. 简历其他方面的 1~2 条改进点；
3. 一句话总体评价。"""

    try:
        client = _get_client()
        resp = client.chat.completions.create(
            model=settings.deepseek_model,
            messages=[
                {"role": "system", "content": "你是资深 HR，给出的建议要具体、可执行、不空泛。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content
    except Exception:
        return None
