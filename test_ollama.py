#!/usr/bin/env python3
"""测试Ollama服务器连接和模型"""
import requests
import json

OLLAMA_URL = "http://10.5.80.8:11434"

# 1. 获取可用模型列表
print("=" * 60)
print("可用模型列表:")
print("=" * 60)
response = requests.get(f"{OLLAMA_URL}/api/tags")
models = response.json()['models']
for model in models:
    print(f"- {model['name']:30} | Size: {model['size'] / (1024**3):.2f} GB")

print("\n" + "=" * 60)
print("推荐的电影专家模型:")
print("=" * 60)
movie_models = [m for m in models if 'movie' in m['name'].lower()]
for model in movie_models:
    print(f"✓ {model['name']}")

# 2. 测试 movie-expert-v3 模型
print("\n" + "=" * 60)
print("测试 movie-expert-v3 模型:")
print("=" * 60)
test_prompt = "推荐一部科幻电影"
print(f"问题: {test_prompt}")

try:
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            'model': 'movie-expert-v3',
            'prompt': test_prompt,
            'stream': False,
            'options': {
                'temperature': 0.3,
                'top_p': 0.7,
                'num_predict': 128
            }
        },
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n回答: {result['response']}")
        print(f"\n✅ 模型测试成功！")
    else:
        print(f"❌ 错误: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ 异常: {e}")
