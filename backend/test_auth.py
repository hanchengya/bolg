#!/usr/bin/env python
"""测试用户认证API"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/auth"

def test_register():
    """测试注册"""
    print("测试用户注册...")
    url = f"{BASE_URL}/register/"
    data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "Test123456!",
        "password_confirm": "Test123456!"
    }
    
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 201:
        return response.json()
    return None

def test_login():
    """测试登录"""
    print("\n测试用户登录...")
    url = f"{BASE_URL}/login/"
    data = {
        "username": "testuser123",
        "password": "Test123456!"
    }
    
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        return response.json()
    return None

def test_get_profile(access_token):
    """测试获取用户信息"""
    print("\n测试获取用户信息...")
    url = "http://localhost:8000/api/v1/auth/me/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    # 测试注册
    register_result = test_register()
    
    # 测试登录
    login_result = test_login()
    
    # 测试获取用户信息
    if login_result and 'access' in login_result:
        test_get_profile(login_result['access'])
    elif register_result and 'access' in register_result:
        test_get_profile(register_result['access'])
    
    print("\n✅ API测试完成！")
