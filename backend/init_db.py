#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建数据库表结构
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.models.database import create_tables

def main():
    """主函数"""
    print("正在初始化数据库...")
    try:
        create_tables()
        print("数据库初始化成功！")
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()