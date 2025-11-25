"""
测试AI模型管理功能
"""
import requests
import json
import sys

# 设置输出编码为UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 配置
BASE_URL = "http://127.0.0.1:8000/api/movies"
OLLAMA_URL = "http://10.5.80.8:11434"

print("=" * 50)
print("AI模型管理功能诊断")
print("=" * 50)

# 1. 测试Ollama服务连接
print("\n[1] 测试Ollama服务连接...")
try:
    response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        print(f"[OK] Ollama服务正常，找到 {len(models)} 个模型")

        # 显示所有模型
        print("\n可用模型列表：")
        for i, model in enumerate(models, 1):
            name = model.get('name', 'unknown')
            size = model.get('size', 0) / (1024**3)
            print(f"  {i}. {name} ({size:.2f} GB)")

        # 检查是否有movie相关模型
        movie_models = [m for m in models if 'movie' in m['name'].lower()]
        print(f"\n包含'movie'的模型: {len(movie_models)} 个")
        for model in movie_models:
            print(f"  - {model['name']}")
    else:
        print(f"[ERROR] Ollama服务响应异常: {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"[ERROR] 无法连接到Ollama服务器 ({OLLAMA_URL})")
    print("   请检查：")
    print("   1. Ollama服务是否启动")
    print("   2. 服务器地址是否正确")
    print("   3. 网络连接是否正常")
except Exception as e:
    print(f"[ERROR] 错误: {e}")

# 2. 测试Django后端API - 获取模型列表
print("\n[2] 测试后端API - 获取模型列表...")
try:
    response = requests.get(f"{BASE_URL}/models/", timeout=10)
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            models = data.get('models', [])
            current = data.get('current_model', '')
            print(f"[OK] 后端API正常，返回 {len(models)} 个movie模型")
            print(f"当前模型: {current}")

            if len(models) == 0:
                print("[WARN] 警告：没有找到包含'movie'关键词的模型")
                print("   建议检查Ollama中是否已安装movie相关模型")
        else:
            error = data.get('error', '未知错误')
            print(f"[ERROR] API返回错误: {error}")
    else:
        print(f"[ERROR] API请求失败")
        try:
            print(f"响应内容: {response.text}")
        except:
            pass
except requests.exceptions.ConnectionError:
    print(f"[ERROR] 无法连接到Django后端 ({BASE_URL})")
    print("   请检查Django服务是否启动")
except Exception as e:
    print(f"[ERROR] 错误: {e}")

# 3. 测试获取当前模型
print("\n[3] 测试获取当前模型...")
try:
    response = requests.get(f"{BASE_URL}/models/current/")
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] 当前使用的模型: {data.get('current_model')}")
    else:
        print(f"[ERROR] 获取失败: {response.status_code}")
except Exception as e:
    print(f"[ERROR] 错误: {e}")

# 4. 测试管理员权限（需要token）
print("\n[4] 测试模型切换API（需要管理员权限）...")
print("请输入管理员的JWT token（留空跳过）：")
token = input().strip()

if token:
    try:
        # 先验证token
        auth_response = requests.get(
            "http://127.0.0.1:8000/api/v1/auth/me/",
            headers={'Authorization': f'Bearer {token}'}
        )

        if auth_response.status_code == 200:
            user_data = auth_response.json()
            username = user_data.get('username', '未知')
            is_staff = user_data.get('is_staff', False)
            is_superuser = user_data.get('is_superuser', False)

            print(f"用户: {username}")
            print(f"管理员: {is_staff}")
            print(f"超级用户: {is_superuser}")

            if not (is_staff or is_superuser):
                print("[ERROR] 当前用户不是管理员，无法切换模型")
            else:
                print("[OK] 用户具有管理员权限")

                # 测试切换模型（使用一个假的模型名称来测试）
                print("\n尝试切换模型（仅测试API，不实际切换）...")
                # 不实际调用切换API，避免误操作
                print("[WARN] 跳过实际切换测试，避免误操作")
        else:
            print(f"[ERROR] Token验证失败: {auth_response.status_code}")
            print("   Token可能已过期或无效")
    except Exception as e:
        print(f"[ERROR] 错误: {e}")
else:
    print("[SKIP] 跳过管理员权限测试")

print("\n" + "=" * 50)
print("诊断完成")
print("=" * 50)

# 总结建议
print("\n[总结] 问题排查建议：")
print("1. 如果Ollama服务连接失败：")
print("   - 检查 backend/apps/movies/ai_config.py 中的 OLLAMA_BASE_URL")
print("   - 确保Ollama服务正在运行")
print("   - 测试命令: curl http://10.5.80.8:11434/api/tags")
print()
print("2. 如果没有找到movie模型：")
print("   - 检查Ollama中是否安装了包含'movie'关键词的模型")
print("   - 可以修改views.py中的过滤条件，显示所有模型")
print()
print("3. 如果权限验证失败：")
print("   - 确保登录的用户是管理员（is_staff=True）")
print("   - 检查JWT token是否有效")
print("   - 尝试重新登录获取新token")
print()
print("4. 如果前端显示错误：")
print("   - 打开浏览器开发者工具查看Console和Network")
print("   - 检查API请求的状态码和响应内容")
