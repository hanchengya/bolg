#!/usr/bin/env python3
"""测试管理员Token和权限"""
import requests
import json

API_BASE = "http://127.0.0.1:8000/api/v1"

print("=" * 60)
print("管理员权限测试工具")
print("=" * 60)

# 获取token
print("\n请输入管理员账户信息：")
username = input("用户名 (默认: admin): ").strip() or "admin"
password = input("密码 (默认: admin123): ").strip() or "admin123"

print("\n" + "=" * 60)
print("1️⃣ 登录并获取Token")
print("=" * 60)

try:
    response = requests.post(
        f"{API_BASE}/auth/login/",
        json={
            'username': username,
            'password': password
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access')
        print(f"✅ 登录成功！")
        print(f"Token: {token[:50]}...")
        
        # 获取用户信息
        print("\n" + "=" * 60)
        print("2️⃣ 获取用户信息")
        print("=" * 60)
        
        me_response = requests.get(
            f"{API_BASE}/auth/me/",
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"✅ 用户信息:")
            print(f"  用户名: {user_data.get('username')}")
            print(f"  邮箱: {user_data.get('email')}")
            print(f"  管理员: {user_data.get('is_staff')} (is_staff)")
            print(f"  超级用户: {user_data.get('is_superuser')} (is_superuser)")
            
            # 测试模型切换
            print("\n" + "=" * 60)
            print("3️⃣ 测试模型切换权限")
            print("=" * 60)
            
            if user_data.get('is_staff') or user_data.get('is_superuser'):
                print("✅ 用户具有管理员权限")
                
                # 测试切换模型
                switch_response = requests.post(
                    "http://127.0.0.1:8000/api/movies/models/switch/",
                    json={'model_name': 'movie-expert-v3:latest'},
                    headers={
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'
                    }
                )
                
                print(f"切换模型API响应: {switch_response.status_code}")
                if switch_response.status_code == 200:
                    result = switch_response.json()
                    if result.get('success'):
                        print(f"✅ 模型切换成功: {result.get('message')}")
                    else:
                        print(f"❌ 切换失败: {result.get('error')}")
                else:
                    print(f"❌ HTTP错误 {switch_response.status_code}")
                    try:
                        error_data = switch_response.json()
                        print(f"错误信息: {error_data}")
                    except:
                        print(f"响应内容: {switch_response.text}")
            else:
                print("❌ 用户不具有管理员权限")
                print("   需要设置 is_staff=True 或 is_superuser=True")
                
        else:
            print(f"❌ 获取用户信息失败: {me_response.status_code}")
            
    else:
        print(f"❌ 登录失败: {response.status_code}")
        print(f"响应: {response.text}")
        
except Exception as e:
    print(f"❌ 异常: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
print("\n如果用户不是管理员，请运行以下命令设置：")
print(f"python manage.py shell -c \"from apps.users.models import User; u=User.objects.get(username='{username}'); u.is_staff=True; u.save(); print('已设置为管理员')\"")
