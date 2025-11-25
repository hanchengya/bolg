"""
AI服务配置
"""

# Ollama服务器配置
OLLAMA_BASE_URL = "http://10.5.80.8:11434"  # Ubuntu服务器

# AI模型配置
OLLAMA_MODEL = "movie-qwen-full:latest"  # 使用最新的v3版本

# 生成参数 - 优化以减少幻觉
OLLAMA_OPTIONS = {
    'temperature': 0.3,      # 降低创造性，提高准确性
    'top_p': 0.7,            # 降低多样性
    'top_k': 20,             # 减少候选词数量
    'repeat_penalty': 1.3,   # 提高重复惩罚
    'num_predict': 256       # 限制最大生成长度，加快速度
}

# 超时设置
OLLAMA_TIMEOUT = 60  # 秒
