#!/usr/bin/env python3
"""快速设置用户为管理员"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.users.models import User

print("=" * 60)
print("设置用户为管理员")
print("=" * 60)

# 列出所有用户
print("\n当前用户列表:")
print("-" * 60)
users = User.objects.all()
for user in users:
    admin_status = ""
    if user.is_superuser:
        admin_status = "🔴 超级管理员"
    elif user.is_staff:
        admin_status = "🟡 管理员"
    else:
        admin_status = "⚪ 普通用户"
    
    print(f"{user.id}. {user.username:15} | {user.email:30} | {admin_status}")

print("\n" + "=" * 60)
username = input("请输入要设置为管理员的用户名: ").strip()

try:
    user = User.objects.get(username=username)
    print(f"\n找到用户: {user.username} ({user.email})")
    print(f"当前状态:")
    print(f"  is_staff: {user.is_staff}")
    print(f"  is_superuser: {user.is_superuser}")
    
    confirm = input("\n是否设置为管理员？(y/n): ").strip().lower()
    if confirm == 'y':
        user.is_staff = True
        user.save()
        print(f"\n✅ 成功！{user.username} 已设置为管理员")
        print(f"   is_staff: {user.is_staff}")
        print(f"   is_superuser: {user.is_superuser}")
    else:
        print("已取消")
        
except User.DoesNotExist:
    print(f"\n❌ 用户 '{username}' 不存在")
except Exception as e:
    print(f"\n❌ 错误: {e}")
