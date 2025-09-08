@echo off

REM StellarChat 后端启动脚本 (Windows)

REM 设置环境变量
set PYTHONPATH=%PYTHONPATH%;%cd%

REM 检查是否安装了Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查是否安装了pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到pip，请先安装pip
    pause
    exit /b 1
)

REM 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt

REM 检查模型目录是否存在
if not exist "models\llm" (
    echo 警告: 未找到模型文件夹 models\llm
    echo 请确保模型文件已放置在正确位置，或通过 MODEL_PATH 环境变量指定模型路径
)

REM 启动应用
echo 正在启动StellarChat后端服务...
echo 访问地址: http://localhost:8000/api/docs 查看API文档

REM 使用uvicorn启动应用
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause