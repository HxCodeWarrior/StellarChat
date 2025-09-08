#!/bin/bash

# StellarChat 后端启动脚本

# 设置环境变量
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 检查是否安装了Python
if ! command -v python3 &> /dev/null
then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查是否安装了pip
if ! command -v pip3 &> /dev/null
then
    echo "错误: 未找到pip3，请先安装pip3"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements.txt

# 检查模型目录是否存在
if [ ! -d "./models/llm" ]; then
    echo "警告: 未找到模型文件夹 ./models/llm"
    echo "请确保模型文件已放置在正确位置，或通过 MODEL_PATH 环境变量指定模型路径"
fi

# 启动应用
echo "正在启动StellarChat后端服务..."
echo "访问地址: http://localhost:8000/api/docs 查看API文档"

# 使用uvicorn启动应用
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload