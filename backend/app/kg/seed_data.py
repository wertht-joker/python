"""预置知识图谱数据：技能词典、岗位要求、学校梯队、公司梯队、证书

所有数据均为纯 Python 结构，由 seed.py 幂等导入 Neo4j。
技能词典同时供「实体抽取」使用（简历文本命中即识别）。
"""

# ===== 技能词典：技能名 -> 类别 =====
SKILLS = {
    # 编程语言
    "Java": "language", "Python": "language", "C++": "language", "C": "language",
    "Go": "language", "JavaScript": "language", "TypeScript": "language",
    "Kotlin": "language", "Rust": "language", "PHP": "language", "Scala": "language",
    "Shell": "language", "SQL": "language",
    # 前端
    "HTML": "frontend", "CSS": "frontend", "HTML5": "frontend", "CSS3": "frontend",
    "Vue": "frontend", "React": "frontend", "Angular": "frontend", "jQuery": "frontend",
    "微信小程序": "frontend", "Webpack": "frontend", "Vite": "frontend", "Node.js": "frontend",
    # 后端框架
    "Spring": "backend", "Spring Boot": "backend", "Spring Cloud": "backend",
    "MyBatis": "backend", "MyBatis-Plus": "backend", "Django": "backend",
    "Flask": "backend", "FastAPI": "backend", "Express": "backend", "Dubbo": "backend",
    "Netty": "backend", "微服务": "backend",
    # 数据库
    "MySQL": "database", "PostgreSQL": "database", "Redis": "database",
    "MongoDB": "database", "Elasticsearch": "database", "Oracle": "database",
    "SQLite": "database", "ClickHouse": "database", "HBase": "database",
    # 中间件 / 消息
    "Kafka": "middleware", "RocketMQ": "middleware", "RabbitMQ": "middleware",
    "Zookeeper": "middleware", "Nginx": "middleware", "Tomcat": "middleware",
    # 大数据
    "Hadoop": "bigdata", "Spark": "bigdata", "Flink": "bigdata", "Hive": "bigdata",
    "HDFS": "bigdata", "Airflow": "bigdata", "数据仓库": "bigdata",
    # 容器 / DevOps
    "Docker": "devops", "Kubernetes": "devops", "Jenkins": "devops",
    "GitLab CI": "devops", "Prometheus": "devops", "Grafana": "devops",
    "持续集成": "devops", "持续部署": "devops",
    # 工具
    "Git": "tool", "Linux": "tool", "Maven": "tool", "Gradle": "tool",
    "IDEA": "tool", "Postman": "tool", "Jupyter": "tool",
    # AI / ML / 数据
    "机器学习": "ai", "深度学习": "ai", "PyTorch": "ai", "TensorFlow": "ai",
    "NLP": "ai", "自然语言处理": "ai", "大模型": "ai", "LLM": "ai",
    "LangChain": "ai", "RAG": "ai", "Milvus": "ai", "Embedding": "ai",
    "向量数据库": "ai", "Prompt工程": "ai", "计算机视觉": "ai", "强化学习": "ai",
    "数据分析": "ai", "统计学": "ai", "pandas": "ai", "NumPy": "ai",
    # 计算机基础
    "数据结构与算法": "cs", "计算机网络": "cs", "操作系统": "cs",
    "数据库原理": "cs", "JVM": "cs", "多线程": "cs", "高并发": "cs",
    "分布式": "cs", "设计模式": "cs",
    # 云
    "AWS": "cloud", "阿里云": "cloud", "腾讯云": "cloud", "华为云": "cloud", "云原生": "cloud",
    # 前端补充
    "HTTP": "frontend", "浏览器原理": "frontend", "性能优化": "frontend", "前端工程化": "frontend",
    # 数据补充
    "Excel": "ai", "数据可视化": "ai", "A/B测试": "ai", "Tableau": "ai", "PowerBI": "ai",
    # 测试
    "测试理论": "test", "接口测试": "test", "自动化测试": "test", "性能测试": "test",
    "测试用例设计": "test", "安全测试": "test",
    # 运维补充
    "监控": "devops", "数据库运维": "devops",
    # 爬虫
    "网络爬虫": "crawler", "Scrapy": "crawler", "BeautifulSoup": "crawler",
    "XPath": "crawler", "正则表达式": "crawler", "反爬": "crawler",
    "数据解析": "crawler", "Selenium": "crawler",
    # Agent
    "LangGraph": "ai", "AI Agent": "ai", "工具调用": "ai",
    "Function Calling": "ai", "多智能体": "ai", "Multi-Agent": "ai",
    # 语言补充
    "C#": "language", "Swift": "language", "Objective-C": "language",
    # 后端补充
    "gRPC": "backend", "Gin": "backend", "CMake": "backend", "QT": "backend",
    # 移动端
    "Android": "mobile", "iOS": "mobile", "Jetpack": "mobile", "Flutter": "mobile",
    "网络编程": "mobile", "架构设计": "mobile",
    # 游戏
    "Unity": "game", "图形学": "game", "游戏引擎": "game",
    "3D数学": "game", "物理引擎": "game",
    # 安全
    "网络安全": "security", "密码学": "security", "渗透测试": "security",
    "漏洞分析": "security", "安全工具": "security", "应急响应": "security",
    "代码审计": "security", "云安全": "security",
    # 嵌入式
    "单片机": "embedded", "嵌入式": "embedded", "RTOS": "embedded", "硬件": "embedded",
    "通信协议": "embedded", "驱动开发": "embedded", "ARM": "embedded", "音视频": "embedded",
    # 数据库补充
    "性能调优": "database", "备份恢复": "database", "分布式数据库": "database",
    # 区块链
    "Solidity": "blockchain", "区块链": "blockchain", "智能合约": "blockchain",
    "共识算法": "blockchain", "以太坊": "blockchain", "Web3": "blockchain",
    # 内存管理
    "内存管理": "cs",
}

# ===== 岗位要求：岗位 -> 分权重要求 =====
JOBS = {
    "Java后端开发": {
        "category": "后端",
        "level": "不限",
        "requires": {
            "核心": ["Java", "Spring Boot", "MySQL", "Redis", "MyBatis", "数据结构与算法"],
            "重要": ["Spring Cloud", "微服务", "Kafka", "RocketMQ", "计算机网络", "Linux", "Git", "SQL", "多线程", "JVM"],
            "加分": ["Docker", "Kubernetes", "高并发", "分布式", "Maven", "Nginx", "设计模式"],
        },
    },
    "前端开发": {
        "category": "前端",
        "level": "不限",
        "requires": {
            "核心": ["JavaScript", "HTML", "CSS", "Vue", "React"],
            "重要": ["TypeScript", "Node.js", "Webpack", "Vite", "HTTP", "Git", "数据结构与算法"],
            "加分": ["微信小程序", "浏览器原理", "性能优化", "前端工程化", "Linux"],
        },
    },
    "算法工程师": {
        "category": "算法",
        "level": "不限",
        "requires": {
            "核心": ["Python", "数据结构与算法", "机器学习", "深度学习", "PyTorch"],
            "重要": ["SQL", "统计学", "Linux", "Git", "TensorFlow", "NumPy"],
            "加分": ["NLP", "大模型", "计算机视觉", "分布式", "强化学习"],
        },
    },
    "数据分析师": {
        "category": "数据",
        "level": "不限",
        "requires": {
            "核心": ["SQL", "Python", "数据分析", "统计学", "Excel"],
            "重要": ["pandas", "NumPy", "数据可视化", "机器学习", "数据仓库"],
            "加分": ["Spark", "Hive", "A/B测试", "Tableau", "PowerBI"],
        },
    },
    "测试开发工程师": {
        "category": "测试",
        "level": "不限",
        "requires": {
            "核心": ["测试理论", "接口测试", "Python", "自动化测试", "Java"],
            "重要": ["性能测试", "测试用例设计", "Linux", "Git", "SQL"],
            "加分": ["持续集成", "安全测试", "Docker", "Jenkins"],
        },
    },
    "运维工程师（SRE）": {
        "category": "运维",
        "level": "不限",
        "requires": {
            "核心": ["Linux", "Docker", "Kubernetes", "计算机网络", "Shell"],
            "重要": ["Python", "持续集成", "持续部署", "监控", "数据库运维", "Nginx"],
            "加分": ["AWS", "阿里云", "Prometheus", "Grafana", "云原生"],
        },
    },
    "Python后端开发": {
        "category": "后端",
        "level": "不限",
        "requires": {
            "核心": ["Python", "Django", "Flask", "FastAPI", "MySQL", "Redis", "数据结构与算法"],
            "重要": ["微服务", "Kafka", "RocketMQ", "计算机网络", "Linux", "Git", "SQL", "Nginx", "多线程"],
            "加分": ["Docker", "Kubernetes", "高并发", "分布式", "设计模式", "云原生"],
        },
    },
    "Python爬虫工程师": {
        "category": "爬虫",
        "level": "不限",
        "requires": {
            "核心": ["Python", "网络爬虫", "Scrapy", "HTTP", "MySQL"],
            "重要": ["BeautifulSoup", "XPath", "正则表达式", "反爬", "数据解析", "Linux", "Git"],
            "加分": ["Selenium", "分布式", "Kafka", "Redis", "Docker"],
        },
    },
    "AI Agent开发工程师": {
        "category": "AI",
        "level": "不限",
        "requires": {
            "核心": ["Python", "LangChain", "大模型", "RAG", "Prompt工程", "数据结构与算法"],
            "重要": ["FastAPI", "LLM", "Milvus", "向量数据库", "Embedding", "SQL", "Linux", "Git", "PyTorch"],
            "加分": ["LangGraph", "AI Agent", "工具调用", "Function Calling", "Docker", "Kubernetes", "NLP"],
        },
    },
    "C++开发工程师": {
        "category": "后端",
        "level": "不限",
        "requires": {
            "核心": ["C++", "数据结构与算法", "操作系统", "计算机网络"],
            "重要": ["多线程", "Linux", "SQL", "设计模式", "内存管理", "数据库原理"],
            "加分": ["高并发", "分布式", "CMake", "QT", "音视频", "gRPC"],
        },
    },
    "Golang开发工程师": {
        "category": "后端",
        "level": "不限",
        "requires": {
            "核心": ["Go", "数据结构与算法", "MySQL", "Redis", "计算机网络"],
            "重要": ["微服务", "Linux", "Git", "SQL", "Docker", "多线程"],
            "加分": ["Kubernetes", "分布式", "高并发", "Kafka", "gRPC", "Gin"],
        },
    },
    "Android开发工程师": {
        "category": "客户端",
        "level": "不限",
        "requires": {
            "核心": ["Java", "Kotlin", "Android", "数据结构与算法"],
            "重要": ["网络编程", "SQL", "Git", "性能优化", "架构设计", "多线程"],
            "加分": ["Jetpack", "Flutter", "Linux", "设计模式"],
        },
    },
    "iOS开发工程师": {
        "category": "客户端",
        "level": "不限",
        "requires": {
            "核心": ["Swift", "Objective-C", "iOS", "数据结构与算法"],
            "重要": ["网络编程", "Git", "性能优化", "架构设计", "多线程"],
            "加分": ["Flutter", "设计模式", "音视频"],
        },
    },
    "大数据开发工程师": {
        "category": "大数据",
        "level": "不限",
        "requires": {
            "核心": ["Hadoop", "Spark", "Hive", "SQL", "Java"],
            "重要": ["Flink", "数据仓库", "HDFS", "Linux", "Python"],
            "加分": ["Kafka", "Airflow", "Kubernetes", "ClickHouse"],
        },
    },
    "数据库工程师（DBA）": {
        "category": "数据库",
        "level": "不限",
        "requires": {
            "核心": ["MySQL", "SQL", "数据库原理", "Linux"],
            "重要": ["PostgreSQL", "Redis", "性能调优", "备份恢复", "数据库运维"],
            "加分": ["分布式数据库", "ClickHouse", "MongoDB", "Oracle"],
        },
    },
    "网络安全工程师": {
        "category": "安全",
        "level": "不限",
        "requires": {
            "核心": ["网络安全", "计算机网络", "Linux", "渗透测试"],
            "重要": ["密码学", "漏洞分析", "Python", "SQL", "安全工具"],
            "加分": ["应急响应", "代码审计", "Docker", "云安全"],
        },
    },
    "嵌入式开发工程师": {
        "category": "嵌入式",
        "level": "不限",
        "requires": {
            "核心": ["C", "C++", "嵌入式", "单片机", "数据结构与算法"],
            "重要": ["RTOS", "Linux", "通信协议", "硬件", "驱动开发"],
            "加分": ["ARM", "音视频", "操作系统"],
        },
    },
    "游戏开发工程师": {
        "category": "游戏",
        "level": "不限",
        "requires": {
            "核心": ["C++", "C#", "Unity", "数据结构与算法", "图形学"],
            "重要": ["游戏引擎", "性能优化", "网络编程", "3D数学"],
            "加分": ["物理引擎", "设计模式", "音视频"],
        },
    },
    "区块链开发工程师": {
        "category": "区块链",
        "level": "不限",
        "requires": {
            "核心": ["Go", "Solidity", "区块链", "智能合约", "数据结构与算法"],
            "重要": ["密码学", "分布式", "共识算法", "Linux", "网络编程"],
            "加分": ["以太坊", "Web3", "gRPC", "Docker"],
        },
    },
}

# 技能权重值（打分用）
WEIGHT_VALUE = {"核心": 1.0, "重要": 0.6, "加分": 0.3}

# ===== 学校梯队 =====
SCHOOLS = {
    "清华大学": "顶尖", "北京大学": "顶尖", "复旦大学": "顶尖", "上海交通大学": "顶尖",
    "浙江大学": "顶尖", "南京大学": "顶尖", "中国科学技术大学": "顶尖",
    "武汉大学": "985", "华中科技大学": "985", "中山大学": "985", "四川大学": "985",
    "西安交通大学": "985", "哈尔滨工业大学": "985", "同济大学": "985", "东南大学": "985",
    "天津大学": "985", "南开大学": "985", "北京航空航天大学": "985", "北京理工大学": "985",
    "中国人民大学": "985", "厦门大学": "985", "山东大学": "985", "中南大学": "985",
    "湖南大学": "985", "吉林大学": "985", "大连理工大学": "985", "电子科技大学": "985",
    "华南理工大学": "985", "重庆大学": "985", "西北工业大学": "985", "兰州大学": "985",
    "东北大学": "985", "中国农业大学": "985", "北京师范大学": "985", "华东师范大学": "985",
    "北京邮电大学": "211", "上海财经大学": "211", "中央财经大学": "211",
    "对外经济贸易大学": "211", "北京交通大学": "211", "北京科技大学": "211",
    "南京航空航天大学": "211", "南京理工大学": "211", "苏州大学": "211",
    "上海大学": "211", "武汉理工大学": "211", "西南交通大学": "211",
    "西南财经大学": "211", "暨南大学": "211", "华南师范大学": "211",
    "华中师范大学": "211", "郑州大学": "211", "西北大学": "211", "福州大学": "211",
    "安徽大学": "211", "云南大学": "211", "哈尔滨工程大学": "211",
    "合肥工业大学": "211", "中国石油大学": "211", "中国地质大学": "211",
    "中国矿业大学": "211", "华北电力大学": "211", "东华大学": "211", "河海大学": "211",
    "江南大学": "211", "西南大学": "211",
}

# ===== 公司梯队 =====
COMPANIES = {
    # 大厂
    "阿里巴巴": "大厂", "腾讯": "大厂", "字节跳动": "大厂", "百度": "大厂",
    "美团": "大厂", "京东": "大厂", "华为": "大厂", "网易": "大厂",
    "拼多多": "大厂", "快手": "大厂", "滴滴": "大厂", "小米": "大厂",
    "蚂蚁集团": "大厂", "微软": "大厂", "Google": "大厂", "Apple": "大厂",
    "小红书": "大厂", "哔哩哔哩": "大厂",
    # 独角兽
    "商汤科技": "独角兽", "旷视科技": "独角兽", "寒武纪": "独角兽", "地平线": "独角兽",
    "大疆": "独角兽", "米哈游": "独角兽", "Shein": "独角兽", "莉莉丝": "独角兽",
    "元气森林": "独角兽", "蜜雪冰城": "独角兽",
    # 中厂
    "携程": "中厂", "新浪": "中厂", "搜狐": "中厂", "360": "中厂",
    "58同城": "中厂", "唯品会": "中厂", "去哪儿": "中厂", "蘑菇街": "中厂",
    "虎牙": "中厂", "斗鱼": "中厂", "阅文集团": "中厂", "完美世界": "中厂",
    "三七互娱": "中厂", "汽车之家": "中厂", "同程旅行": "中厂", "顺丰科技": "中厂",
}

# ===== 证书：名称 -> 加分值 =====
CERTIFICATES = {
    "大学英语四级": 4, "大学英语六级": 8, "英语四级": 4, "英语六级": 8,
    "CET-6": 8, "CET-4": 4,
    "计算机二级": 3, "计算机三级": 5, "计算机四级": 6,
    "软考初级": 3, "软考中级": 8, "软考高级": 15,
    "托福": 6, "雅思": 6, "GRE": 4,
    "教师资格证": 2, "普通话": 2,
    "CPA": 10, "ACCA": 8, "证券从业资格证": 3, "基金从业资格证": 3,
    "专利": 10, "论文": 6,
}
