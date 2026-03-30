# Skin Diseases

皮肤病图像分类项目，使用深度学习模型进行皮肤病变识别。

## 项目结构

```
Skin diseases/
├── HAM10000/          # HAM10000 数据集
├── agent/             # Agent 相关代码
├── skin diseases/    # 皮肤病数据集
├── chroma_db/         # Chroma 向量数据库
├── config/            # 配置文件
├── data/              # 数据目录
├── frontend/          # 前端代码
├── logs/              # 日志文件
├── model/             # 模型文件
├── pretrained/        # 预训练模型
├── prompts/           # 提示词模板
├── rag/               # RAG 相关代码
├── run/               # 运行脚本
├── runs/              # 训练运行记录
├── test/              # 测试代码
├── utils/             # 工具函数
├── variables/         # 变量配置
├── yolo_variables/    # YOLO 配置
├── app.py             # Web 应用入口
├── dataset_split.py   # 数据集划分
├── evaluate.py        # 模型评估
├── main.py            # 主程序
├── run_agent.py       # Agent 运行脚本
├── test.py            # 测试脚本
├── train_validation.py# 训练验证脚本
├── yolo_main.py       # YOLO 主程序
└── yolov10n.pt        # YOLO 预训练权重
```

## 环境要求

- Python 3.8+
- PyTorch
- 相关依赖包

## 使用方法

### 训练模型
分类
```bash
python main --val True 
```
yolo
```bash
python  yolo_main.py
```
### 评估模型
```bash
python evaluate.py
```

### 启动 Web 应用
前提要在 "E:\py项目\Skin diseases\frontend"目录下运行
```bash
streamlit run main_app.py
```

### 运行 Agent
```bash
python run_agent.py
```

## 主要功能

- 皮肤病变图像分类
- RAG 增强诊断
- YOLO 目标检测
- Web 界面交互
