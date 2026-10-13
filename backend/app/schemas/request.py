"""请求模型"""
from pydantic import BaseModel


class GradeRequest(BaseModel):
    """打分请求"""
    resume_text: str      # 简历文本
    job: str              # 目标岗位名称
