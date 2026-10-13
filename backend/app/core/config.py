"""全局配置管理：从 .env / 环境变量读取"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ===== 应用 =====
    app_name: str = "简历打分助手"

    # ===== Neo4j =====
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "neo4j"

    # ===== DeepSeek =====
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    # ===== 打分维度权重（合计为 1）=====
    w_skill: float = 0.40        # 技能匹配
    w_education: float = 0.20    # 学历背景
    w_project: float = 0.20      # 项目经验
    w_experience: float = 0.15   # 实习/工作经历
    w_certificate: float = 0.05  # 证书加分


settings = Settings()
