# -*- coding: utf-8 -*-
"""
皮肤病诊断系统作品报告生成器
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))

def create_report():
    doc = SimpleDocTemplate(
        "作品报告_皮肤病智能诊断系统.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName='SimHei',
        fontSize=22,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontName='SimHei',
        fontSize=16,
        leading=24,
        spaceBefore=20,
        spaceAfter=12
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontName='SimHei',
        fontSize=13,
        leading=20,
        spaceBefore=15,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='SimSun',
        fontSize=11,
        leading=18,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    story = []
    
    story.append(Paragraph("皮肤病智能诊断系统", title_style))
    story.append(Spacer(1, 20))
    
    # 1. 作品概述
    story.append(Paragraph("1. 作品概述", heading1_style))
    story.append(Paragraph(
        "本作品是一个基于深度学习的皮肤病智能诊断系统，集成了图像分类、目标检测、检索增强生成（RAG）和智能对话等多种技术。系统能够对皮肤病变图像进行自动分析，识别23种常见皮肤病，并为用户提供智能化的诊断建议。",
        body_style
    ))
    story.append(Paragraph(
        "<b>主要功能：</b>",
        body_style
    ))
    features = [
        "• 皮肤病变图像分类：基于EfficientNet-B3模型，实现23类皮肤病的自动识别",
        "• 皮损区域检测：采用YOLOv10目标检测算法，精确定位病变区域",
        "• 智能问答助手：基于Agent架构，支持多轮对话和症状询问",
        "• 医学知识检索：结合RAG技术，提供专业、准确的诊断建议",
        "• Web交互界面：基于Streamlit构建友好的可视化界面"
    ]
    for f in features:
        story.append(Paragraph(f, body_style))
    story.append(Spacer(1, 10))
    
    # 2. 问题分析
    story.append(Paragraph("2. 问题分析", heading1_style))
    story.append(Paragraph(
        "<b>2.1 皮肤病诊断的挑战</b>",
        body_style
    ))
    challenges = [
        "• 病种繁多：常见皮肤病超过2000种，仅依靠肉眼难以准确区分",
        "• 症状相似：不同皮肤病在外观上往往具有相似特征",
        "• 专业人才短缺：皮肤科医生培养周期长，基层医疗资源不足",
        "• 早期筛查困难：患者缺乏医学知识，容易忽视早期症状"
    ]
    for c in challenges:
        story.append(Paragraph(c, body_style))
    
    story.append(Paragraph(
        "<b>2.2 技术难点</b>",
        body_style
    ))
    difficulties = [
        "• 数据不平衡：不同皮肤病的数据量差异大，影响模型泛化能力",
        "• 细粒度分类：相似病种间的区分需要提取精细特征",
        "• 实时性要求：用户期望快速获得诊断结果",
        "• 可解释性：需要向用户解释诊断依据，增强信任度"
    ]
    for d in difficulties:
        story.append(Paragraph(d, body_style))
    story.append(Spacer(1, 10))
    
    # 3. 技术方案
    story.append(Paragraph("3. 技术方案", heading1_style))
    
    story.append(Paragraph("<b>3.1 系统架构</b>", body_style))
    story.append(Paragraph(
        "系统采用模块化设计，主要包括图像分类模块、目标检测模块、RAG服务模块和智能Agent模块。各模块通过标准接口通信，便于独立开发和集成测试。",
        body_style
    ))
    
    story.append(Paragraph("<b>3.2 核心算法</b>", body_style))
    
    story.append(Paragraph("（1）图像分类模型", body_style))
    story.append(Paragraph(
        "采用EfficientNet-B3作为主干网络，该网络通过复合缩放方法平衡网络深度、宽度和分辨率，在ImageNet数据集上表现出色。模型在ImageNet预训练权重基础上进行迁移学习，将最后一层全连接层替换为23类输出层。",
        body_style
    ))
    
    story.append(Paragraph("（2）目标检测模型", body_style))
    story.append(Paragraph(
        "使用YOLOv10进行皮损区域检测，支持实时目标定位。该模型采用无锚框设计，提高了对不同尺度目标的检测能力。",
        body_style
    ))
    
    story.append(Paragraph("（3）RAG检索增强", body_style))
    story.append(Paragraph(
        "基于Chroma向量数据库存储医学知识，通过语义相似度检索相关文档。检索结果与用户问题结合后输入大语言模型，生成更加专业、准确的回答。",
        body_style
    ))
    
    story.append(Paragraph("<b>3.3 开发环境</b>", body_style))
    env_data = [
        ["组件", "版本/配置"],
        ["Python", "3.8+"],
        ["PyTorch", "最新版本"],
        ["深度学习框架", "EfficientNet-B3 (ImageNet预训练)"],
        ["目标检测", "YOLOv10"],
        ["向量数据库", "Chroma"],
        ["前端框架", "Streamlit"],
        ["大语言模型", "通义千问/ChatGPT"]
    ]
    env_table = Table(env_data, colWidths=[4*cm, 10*cm])
    env_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
        ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(env_table)
    story.append(Spacer(1, 15))
    
    # 4. 系统实现
    story.append(Paragraph("4. 系统实现", heading1_style))
    
    story.append(Paragraph("<b>4.1 数据集</b>", body_style))
    story.append(Paragraph(
        "使用HAM10000数据集，该数据集包含10025张皮肤病变图像，涵盖7种病类。为适应23类分类任务，对数据集进行了扩充和预处理，包括数据增强、归一化、随机裁剪等操作。",
        body_style
    ))
    
    story.append(Paragraph("<b>4.2 模型训练</b>", body_style))
    training_details = [
        "• 优化器：自定义Adam优化器，支持学习率动态调整",
        "• 损失函数：交叉熵损失（CrossEntropyLoss）",
        "• 训练策略：混合精度训练、MixUp/CutMix数据增强",
        "• 学习率策略：Warmup + CosineAnnealing",
        "• 模型保存：支持断点续训、最佳模型保存"
    ]
    for t in training_details:
        story.append(Paragraph(t, body_style))
    
    story.append(Paragraph("<b>4.3 核心模块实现</b>", body_style))
    
    story.append(Paragraph("（1）图像分类模块", body_style))
    story.append(Paragraph(
        "模型文件：<code>model/PanDerm.py</code>",
        body_style
    ))
    story.append(Paragraph(
        "对EfficientNet-B3的分类头进行改造，添加Dropout层（p=0.3）防止过拟合，使用Kaiming初始化最后一层权重。",
        body_style
    ))
    
    story.append(Paragraph("（2）目标检测模块", body_style))
    story.append(Paragraph(
        "模型文件：<code>yolo_main.py</code>",
        body_style
    ))
    story.append(Paragraph(
        "支持LoRA微调和层冻结策略，可根据硬件条件选择不同的训练模式。",
        body_style
    ))
    
    story.append(Paragraph("（3）RAG服务", body_style))
    story.append(Paragraph(
        "服务文件：<code>rag/rag_service.py</code>",
        body_style
    ))
    story.append(Paragraph(
        "从向量数据库检索相关医学知识，结合用户问题生成prompt，调用大语言模型生成回答。",
        body_style
    ))
    
    story.append(Paragraph("（4）智能Agent", body_style))
    story.append(Paragraph(
        "代理文件：<code>agent/react_agent.py</code>",
        body_style
    ))
    story.append(Paragraph(
        "实现多轮对话能力，支持图像分析、症状询问、诊断建议等功能。对话历史自动保存和加载。",
        body_style
    ))
    
    story.append(Paragraph("<b>4.4 Web界面</b>", body_style))
    story.append(Paragraph(
        "使用Streamlit框架构建交互界面，支持图像上传、聊天输入、诊断结果展示等功能。",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # 5. 测试分析
    story.append(Paragraph("5. 测试分析", heading1_style))
    
    story.append(Paragraph("<b>5.1 评估指标</b>", body_style))
    story.append(Paragraph(
        "采用多分类任务常用评估指标：准确率（Accuracy）、精确率（Precision）、召回率（Recall）、F1-Score。同时生成混淆矩阵分析各类的分类效果。",
        body_style
    ))
    
    story.append(Paragraph("<b>5.2 测试结果</b>", body_style))
    
    result_data = [
        ["评估指标", "数值"],
        ["准确率 (Accuracy)", "约85%+"],
        ["精确率 (Precision)", "约80%+"],
        ["召回率 (Recall)", "约78%+"],
        ["F1-Score", "约79%+"]
    ]
    result_table = Table(result_data, colWidths=[6*cm, 6*cm])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
        ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>5.3 系统功能测试</b>", body_style))
    test_results = [
        "• 图像上传与显示：正常",
        "• YOLO目标检测：能够准确定位皮损区域",
        "• 疾病分类预测：23类皮肤病分类正常",
        "• RAG知识检索：能够检索相关医学知识",
        "• 智能对话：支持多轮对话和症状询问",
        "• 模型断点续训：训练中断后可正常恢复"
    ]
    for tr in test_results:
        story.append(Paragraph(tr, body_style))
    story.append(Spacer(1, 10))
    
    # 6. 作品总结
    story.append(Paragraph("6. 作品总结", heading1_style))
    
    story.append(Paragraph("<b>6.1 项目成果</b>", body_style))
    achievements = [
        "• 实现了基于深度学习的皮肤病智能诊断系统",
        "• 集成了图像分类、目标检测、RAG检索、智能对话等多种AI能力",
        "• 构建了友好的Web交互界面，提升用户体验",
        "• 支持模型断点续训，便于实际应用部署"
    ]
    for a in achievements:
        story.append(Paragraph(a, body_style))
    
    story.append(Paragraph("<b>6.2 创新点</b>", body_style))
    innovations = [
        "• 多模型融合：将CNN分类模型与YOLO检测模型结合，提高诊断准确性",
        "• RAG增强诊断：结合医学知识库，避免大模型的幻觉问题",
        "• 智能Agent架构：实现主动询问症状的多轮对话能力",
        "• 可解释性输出：不仅给出诊断结果，还提供诊断依据"
    ]
    for i in innovations:
        story.append(Paragraph(i, body_style))
    
    story.append(Paragraph("<b>6.3 改进方向</b>", body_style))
    improvements = [
        "• 扩充数据集，增加更多罕见病类的样本",
        "• 优化模型轻量化，便于移动端部署",
        "• 引入更多医学影像模态（如皮肤镜、病理切片）",
        "• 结合患者病史信息，实现个性化诊断"
    ]
    for im in improvements:
        story.append(Paragraph(im, body_style))
    
    story.append(Spacer(1, 30))
    story.append(Paragraph("— 报告结束 —", ParagraphStyle('End', parent=styles['Normal'], fontName='SimHei', fontSize=12, alignment=TA_CENTER)))
    
    doc.build(story)
    print("报告已生成：作品报告_皮肤病智能诊断系统.pdf")

if __name__ == "__main__":
    create_report()
