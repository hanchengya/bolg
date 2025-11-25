#!/usr/bin/env python
"""
测试AI聊天接口
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_chat_api():
    """测试聊天API"""
    print("=" * 60)
    print("测试电影AI聊天接口")
    print("=" * 60)
    
    test_questions = [
        "杨丽老师是谁？",
        "《四川交院的生活》是什么类型的电影？",
        "《四川交院的生活》的豆瓣评分是多少？",
        "推荐一部科幻电影",
        "推荐一部悬疑电影",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n【测试 {i}/{len(test_questions)}】")
        print(f"问题: {question}")
        print("-" * 60)
        
        try:
            start_time = time.time()
            
            response = requests.post(
                f"{API_BASE_URL}/api/movies/chat/",
                json={"message": question},
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ 回答: {data['response']}")
                    print(f"⏱️ 耗时: {elapsed_time:.2f}秒")
                else:
                    print(f"❌ 错误: {data.get('error')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"响应: {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ 请求超时（60秒）")
        except requests.exceptions.ConnectionError:
            print("🔌 连接失败，请检查Django服务是否运行")
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        
        # 避免请求过快
        if i < len(test_questions):
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)


def test_recommend_api():
    """测试推荐API"""
    print("\n" + "=" * 60)
    print("测试电影推荐接口")
    print("=" * 60)
    
    genres = ["科幻", "悬疑", "动作", ""]
    
    for genre in genres:
        genre_text = genre if genre else "任意类型"
        print(f"\n【推荐 {genre_text}】")
        print("-" * 60)
        
        try:
            start_time = time.time()
            
            response = requests.post(
                f"{API_BASE_URL}/api/movies/recommend/",
                json={"genre": genre},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ 推荐: {data['recommendation']}")
                    print(f"⏱️ 耗时: {elapsed_time:.2f}秒")
                else:
                    print(f"❌ 错误: {data.get('error')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("✅ 推荐测试完成")
    print("=" * 60)


def check_ollama_status():
    """检查Ollama服务状态"""
    print("=" * 60)
    print("检查Ollama服务状态")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("✅ Ollama服务正常运行")
            print(f"\n已加载的模型:")
            for model in models:
                print(f"  - {model['name']}")
            
            # 检查movie-expert-v3是否存在
            model_names = [m['name'] for m in models]
            if 'movie-expert-v3:latest' in model_names or 'movie-expert-v3' in [m['name'].split(':')[0] for m in models]:
                print("\n✅ movie-expert-v3 模型已就绪")
                return True
            else:
                print("\n⚠️ 警告: movie-expert-v3 模型未找到")
                print("请运行: ollama create movie-expert-v3 -f Modelfile.v3")
                return False
        else:
            print(f"❌ Ollama服务异常: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Ollama服务")
        print("请确保Ollama正在运行: ollama serve")
        return False
    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")
        return False


def check_django_status():
    """检查Django服务状态"""
    print("\n" + "=" * 60)
    print("检查Django服务状态")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/movies/", timeout=5)
        if response.status_code == 200:
            print("✅ Django服务正常运行")
            return True
        else:
            print(f"⚠️ Django服务响应异常: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Django服务")
        print("请启动Django: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n🎬 电影AI助手测试工具\n")
    
    # 检查服务状态
    ollama_ok = check_ollama_status()
    django_ok = check_django_status()
    
    if not ollama_ok or not django_ok:
        print("\n" + "=" * 60)
        print("⚠️ 请先确保所有服务正常运行")
        print("=" * 60)
        exit(1)
    
    # 运行测试
    try:
        test_chat_api()
        test_recommend_api()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试完成！")
        print("=" * 60)
        print("\n下一步:")
        print("1. 启动前端: cd frontend && npm run dev")
        print("2. 访问: http://localhost:5173")
        print("3. 点击右下角悬浮按钮开始聊天")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 测试已中断")
