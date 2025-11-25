"""
测试模型切换功能（需要管理员Token）
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("测试模型切换功能")
print("=" * 60)

# 获取管理员Token
print("\n[1] 请输入管理员用户名和密码以获取Token")
username = input("用户名: ").strip()
password = input("密码: ").strip()

if not username or not password:
    print("[ERROR] 用户名或密码不能为空")
    exit(1)

# 登录获取Token
print("\n[2] 正在登录...")
try:
    login_response = requests.post(
        f"{BASE_URL}/api/v1/auth/login/",
        json={"username": username, "password": password}
    )

    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data.get('access')
        print(f"[OK] 登录成功")

        # 验证用户权限
        me_response = requests.get(
            f"{BASE_URL}/api/v1/auth/me/",
            headers={'Authorization': f'Bearer {token}'}
        )

        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"\n用户信息：")
            print(f"  用户名: {user_data.get('username')}")
            print(f"  邮箱: {user_data.get('email')}")
            print(f"  管理员: {user_data.get('is_staff')}")
            print(f"  超级用户: {user_data.get('is_superuser')}")

            if not (user_data.get('is_staff') or user_data.get('is_superuser')):
                print("\n[ERROR] 当前用户没有管理员权限，无法切换模型")
                exit(1)
        else:
            print(f"[ERROR] 获取用户信息失败: {me_response.status_code}")
            exit(1)
    else:
        print(f"[ERROR] 登录失败: {login_response.status_code}")
        print(f"响应: {login_response.text}")
        exit(1)
except Exception as e:
    print(f"[ERROR] 登录过程出错: {e}")
    exit(1)

# 获取可用模型列表
print("\n[3] 获取可用模型列表...")
try:
    models_response = requests.get(f"{BASE_URL}/api/movies/models/")

    if models_response.status_code == 200:
        data = models_response.json()
        if data.get('success'):
            models = data.get('models', [])
            current_model = data.get('current_model', '')

            print(f"[OK] 找到 {len(models)} 个可用模型")
            print(f"\n当前使用的模型: {current_model}")
            print("\n可用模型列表：")

            for i, model in enumerate(models, 1):
                status = " [当前]" if model.get('is_current') else ""
                print(f"  {i}. {model.get('name')}{status}")
                print(f"     大小: {model.get('size')}")

            # 选择要切换的模型
            if len(models) <= 1:
                print("\n[WARN] 只有一个模型，无需切换")
                exit(0)

            print("\n[4] 选择要切换的模型")
            print("请输入模型编号（1-{}），或输入 0 取消: ".format(len(models)))
            choice = input().strip()

            try:
                choice_num = int(choice)
                if choice_num == 0:
                    print("[SKIP] 已取消")
                    exit(0)

                if choice_num < 1 or choice_num > len(models):
                    print("[ERROR] 无效的选择")
                    exit(1)

                target_model = models[choice_num - 1]
                target_model_name = target_model.get('name')

                if target_model.get('is_current'):
                    print(f"[WARN] 模型 {target_model_name} 已经是当前使用的模型")
                    exit(0)

                # 执行切换
                print(f"\n[5] 正在切换到模型: {target_model_name}")
                switch_response = requests.post(
                    f"{BASE_URL}/api/movies/models/switch/",
                    json={"model_name": target_model_name},
                    headers={
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'
                    }
                )

                print(f"响应状态码: {switch_response.status_code}")
                print(f"响应内容: {switch_response.text}")

                if switch_response.status_code == 200:
                    result = switch_response.json()
                    if result.get('success'):
                        print(f"\n[OK] {result.get('message')}")
                        print(f"当前模型: {result.get('current_model')}")

                        # 验证切换是否成功
                        print("\n[6] 验证切换结果...")
                        verify_response = requests.get(f"{BASE_URL}/api/movies/models/current/")
                        if verify_response.status_code == 200:
                            verify_data = verify_response.json()
                            actual_model = verify_data.get('current_model')
                            print(f"实际当前模型: {actual_model}")

                            if actual_model == target_model_name or actual_model.startswith(target_model_name):
                                print("\n[SUCCESS] 模型切换成功！")
                            else:
                                print(f"\n[WARN] 模型可能未正确切换")
                        else:
                            print("[ERROR] 无法验证切换结果")
                    else:
                        print(f"\n[ERROR] 切换失败: {result.get('error')}")
                else:
                    print(f"\n[ERROR] 切换请求失败")

            except ValueError:
                print("[ERROR] 请输入有效的数字")
                exit(1)
        else:
            print(f"[ERROR] {data.get('error')}")
    else:
        print(f"[ERROR] 获取模型列表失败: {models_response.status_code}")
except Exception as e:
    print(f"[ERROR] 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
