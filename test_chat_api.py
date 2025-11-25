#!/usr/bin/env python3
"""测试后端AI聊天API"""
import requests
import json

API_URL = "http://127.0.0.1:8000/api/movies/chat/"

test_messages = [
    "推荐一部科幻电影",
    "肖申克的救赎好看吗？",
    "有哪些高分的动作片？"
]

print("=" * 60)
print("测试后端 AI 聊天 API")
print("=" * 60)

for i, message in enumerate(test_messages, 1):
    print(f"\n测试 {i}: {message}")
    print("-" * 60)
    
    try:
        response = requests.post(
            API_URL,
            json={'message': message},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ 成功!")
                print(f"回答: {result.get('response', '')[:200]}...")
            else:
                print(f"❌ 失败: {result.get('error')}")
        else:
            print(f"❌ HTTP {response.status_code}")
            print(response.text[:200])
    except Exception as e:
        print(f"❌ 异常: {e}")

print("\n" + "=" * 60)
print("测试完成!")
print("=" * 60)
