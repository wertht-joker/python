"""抽取辅助数据：技能别名归一化、学历/证书识别规则"""

# 简历常见写法 -> 标准技能名（归一化后再匹配词典）
SKILL_ALIASES = {
    "K8s": "Kubernetes", "k8s": "Kubernetes", "K8S": "Kubernetes",
    "SpringBoot": "Spring Boot", "springboot": "Spring Boot",
    "SpringMVC": "Spring", "springmvc": "Spring",
    "MyBatisPlus": "MyBatis-Plus", "mybatisplus": "MyBatis-Plus",
    "Vue3": "Vue", "vue3": "Vue", "Vue.js": "Vue", "vue.js": "Vue",
    "React.js": "React", "react.js": "React",
    "Node": "Node.js", "node.js": "Node.js", "NodeJS": "Node.js",
    "Mysql": "MySQL", "mysql": "MySQL",
    "ElasticSearch": "Elasticsearch", "elasticsearch": "Elasticsearch",
    "Postgres": "PostgreSQL", "postgres": "PostgreSQL",
    "kafka": "Kafka", "redis": "Redis", "docker": "Docker",
    "Kubernetes": "Kubernetes",
    "大语言模型": "大模型", "大模型技术": "大模型",
}

# 学历识别（按优先级从上到下，先命中哪个算哪个）
EDUCATION_LEVELS = [
    ("博士", "博士"),
    ("硕士", "硕士"),
    ("研究生", "硕士"),
    ("本科", "本科"),
    ("学士", "本科"),
    ("专科", "专科"),
    ("大专", "专科"),
]
