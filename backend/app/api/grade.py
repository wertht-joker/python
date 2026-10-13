"""打分接口"""
from fastapi import APIRouter

from app.extract import extractor
from app.schemas.request import GradeRequest
from app.scoring import advice, grader

router = APIRouter(tags=["简历打分"])


@router.post("/grade")
def grade(req: GradeRequest):
    if not req.resume_text.strip():
        return {"code": 400, "message": "简历内容为空", "data": None}

    try:
        entities = extractor.extract(req.resume_text)
        result = grader.grade(entities, req.job)
    except ValueError as e:
        return {"code": 400, "message": str(e), "data": None}
    except Exception as e:
        return {"code": 500, "message": f"打分失败: {e}", "data": None}

    # LLM 生成改进建议（未配置 Key 时为 None，前端提示）
    result["advice"] = advice.generate_advice(entities, result)
    # 附上抽取到的实体，前端展示「识别出了什么」
    result["entities"] = entities
    return {"code": 200, "message": "ok", "data": result}
