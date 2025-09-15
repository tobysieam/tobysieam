# 软件工程第二次作业-个人项目

## 项目简介
本项目实现了一个简单的论文查重工具，支持通过命令行参数输入原文、抄袭版和输出文件路径，输出重复率（保留两位小数）。

## 使用方法
```bash
python main.py [原文文件] [抄袭版论文的文件] [答案文件]
```

## 依赖安装
```bash
pip install -r requirements.txt
```

## 主要文件说明
- main.py：程序入口
- checker.py：查重算法实现
- utils.py：工具函数
- test_checker.py：单元测试
- requirements.txt：依赖包

