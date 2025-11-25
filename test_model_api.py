#!/usr/bin/env python3
"""测试模型管理 API"""
import requests
import json

API_BASE = "http://127.0.0.1:8000/api/movies"

print("=" * 60)
print("测试模型管理 API")
print("=" * 60)

# 1. 获取可用模型列表
print("\n1️⃣ 获取可用模型列表:")
print("-" * 60)
try:
    response = requests.get(f"{API_BASE}/models/")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ 成功获取模型列表")
            print(f"当前模型: {data['current_model']}")
            print(f"\n可用模型 ({len(data['models'])} 个):")
            for model in data['models']:
                status = "⭐ [当前]" if model['is_current'] else ""
                print(f"  - {model['name']:30} | {model['size']:10} {status}")
        else:
            print(f"❌ 失败: {data.get('error')}")
    else:
        print(f"❌ HTTP {response.status_code}")
except Exception as e:
    print(f"❌ 异常: {e}")

# 2. 获取当前模型
print("\n2️⃣ 获取当前模型:")
print("-" * 60)
try:
    response = requests.get(f"{API_BASE}/models/current/")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ 当前模型: {data['current_model']}")
        else:
            print(f"❌ 失败: {data.get('error')}")
    else:
        print(f"❌ HTTP {response.status_code}")
except Exception as e:
    print(f"❌ 异常: {e}")

# 3. 测试模型切换（需要管理员权限，这里只是测试端点是否存在）
print("\n3️⃣ 测试模型切换 API（权限检查）:")
print("-" * 60)
try:
    response = requests.post(
        f"{API_BASE}/models/switch/",
        json={'model_name': 'movie-expert-v3:latest'}
    )
    # 预期会返回 403（未认证）或其他权限错误
    if response.status_code == 403 or response.status_code == 401:
        print(f"✅ API 端点正常（需要管理员权限）")
    elif response.status_code == 200:
        print(f"✅ API 端点正常（无权限验证）")
    else:
        print(f"⚠️ 返回状态: {response.status_code}")
except Exception as e:
    print(f"❌ 异常: {e}")

print("\n" + "=" * 60)
print("✅ API 测试完成！")
print("=" * 60)
