import requests
import json
import time

# API配置
BASE_URL = "http://localhost:8080/api"
MODEL_NAME = "stellar-byte-llm"

def test_list_models():
    """测试获取模型列表接口"""
    print("测试获取模型列表接口...")
    url = f"{BASE_URL}/models"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 成功获取模型列表: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"✗ 获取模型列表失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False

def test_chat_completion_non_streaming():
    """测试非流式聊天完成接口"""
    print("\n测试非流式聊天完成接口...")
    url = f"{BASE_URL}/chat/completions"
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": "你好，世界！"}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 非流式聊天完成成功: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"✗ 非流式聊天完成失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False

def test_chat_completion_streaming():
    """测试流式聊天完成接口"""
    print("\n测试流式聊天完成接口...")
    url = f"{BASE_URL}/chat/completions"
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": "请给我讲一个关于人工智能的短故事。"}
        ],
        "temperature": 0.7,
        "max_tokens": 200,
        "stream": True
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)
        if response.status_code == 200:
            print("✓ 流式聊天完成开始:")
            print("Assistant: ", end="", flush=True)
            
            # 简单解析SSE流
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        data = decoded_line[6:]  # 移除 'data: ' 前缀
                        if data != '[DONE]':
                            try:
                                chunk = json.loads(data)
                                if 'choices' in chunk and len(chunk['choices']) > 0:
                                    delta = chunk['choices'][0]['delta']
                                    if 'content' in delta and delta['content']:
                                        print(delta['content'], end="", flush=True)
                            except json.JSONDecodeError:
                                pass  # 忽略解析错误
            print("\n✓ 流式聊天完成结束")
            return True
        else:
            print(f"✗ 流式聊天完成失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False

def test_chat_completion_with_history():
    """测试带对话历史的聊天完成接口"""
    print("\n测试带对话历史的聊天完成接口...")
    url = f"{BASE_URL}/chat/completions"
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": "你好，我叫小明。"},
            {"role": "assistant", "content": "你好，小明！很高兴认识你。有什么我可以帮助你的吗？"},
            {"role": "user", "content": "你知道我的名字吗？"}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 带对话历史的聊天完成成功: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"✗ 带对话历史的聊天完成失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False

def test_invalid_model():
    """测试无效模型请求"""
    print("\n测试无效模型请求...")
    url = f"{BASE_URL}/chat/completions"
    
    payload = {
        "model": "invalid-model",
        "messages": [
            {"role": "user", "content": "你好"}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 400:
            print(f"✓ 正确拒绝无效模型请求: {response.status_code} - {response.text}")
            return True
        else:
            print(f"✗ 未正确拒绝无效模型请求: 期望400，实际{response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("开始测试聊天完成接口...")
    print("=" * 50)
    
    # 测试获取模型列表
    test_list_models()
    
    # 测试非流式聊天完成
    test_chat_completion_non_streaming()
    
    # 测试流式聊天完成
    test_chat_completion_streaming()
    
    # 测试带对话历史的聊天完成
    test_chat_completion_with_history()
    
    # 测试无效模型请求
    test_invalid_model()
    
    print("\n" + "=" * 50)
    print("聊天完成接口测试完成")

if __name__ == "__main__":
    main()