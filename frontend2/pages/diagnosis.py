"""
诊断分析页面
图像上传、YOLO检测框可视化、分类结果显示、Top-5概率列表
"""

import streamlit as st
import requests
import json
import time
import tempfile
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64

st.set_page_config(page_title="诊断分析", page_icon="📊", layout="wide")

# 页面标题
st.title("📊 诊断分析")
st.markdown("上传皮肤病变图像，AI将自动进行YOLO目标检测和CNN分类")

# API地址配置
API_BASE = "http://localhost:8000"

# 初始化会话状态
if "current_diagnosis" not in st.session_state:
    st.session_state["current_diagnosis"] = None
if "detection_result" not in st.session_state:
    st.session_state["detection_result"] = None


def draw_detection_boxes(image, boxes, labels, confidences):
    """在图像上绘制检测框"""
    img = image.copy()
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"]
    
    for i, (box, label, conf) in enumerate(zip(boxes, labels, confidences)):
        x1, y1, x2, y2 = map(int, box)
        color = colors[i % len(colors)]
        
        # 绘制矩形框
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        
        # 绘制标签背景
        text = f" {label} {conf:.2f}"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        draw.rectangle([x1, y1 - text_height - 10, x1 + text_width + 10, y1], fill=color)
        draw.text((x1 + 5, y1 - text_height - 5), text, fill="white", font=font)
    
    return img


def image_to_base64(img):
    """将PIL图像转换为base64"""
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


# 主界面布局
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📤 图像上传")
    
    # 模型选择
    model_option = st.selectbox(
        "选择分类模型",
        ["EfficientNet-B3 (推荐)", "ResNet50"],
        help="EfficientNet-B3精度更高，ResNet50速度更快"
    )
    model_name = "efficientnet_b3" if "EfficientNet" in model_option else "resnet50"
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "选择皮肤病变图像",
        type=["jpg", "jpeg", "png"],
        help="支持 JPG、PNG 格式，建议图片清晰、光照均匀"
    )
    
    if uploaded_file:
        # 显示原始图像
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="原始图像", use_container_width=True)
        
        # 分析按钮
        if st.button("🔍 开始诊断", type="primary", use_container_width=True):
            with st.spinner("正在分析图像..."):
                # 模拟API调用（实际需要连接后端）
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    ("正在预处理图像...", 20),
                    ("正在进行YOLO目标检测...", 50),
                    ("正在提取皮损区域...", 70),
                    ("正在进行CNN分类...", 90),
                    ("正在生成诊断报告...", 100)
                ]
                
                for step_text, progress in steps:
                    status_text.text(step_text)
                    progress_bar.progress(progress)
                    time.sleep(0.5)
                
                # 模拟检测结果（实际应该调用后端API）
                boxes = [[50, 30, 250, 230]]
                labels = ["病变区域"]
                confidences = [0.95]
                
                # 绘制检测框
                result_image = draw_detection_boxes(image, boxes, labels, confidences)
                
                # 模拟分类结果
                top5_results = [
                    {"class": "银屑病", "class_en": "Psoriasis", "probability": 0.87},
                    {"class": "湿疹", "class_en": "Eczema", "probability": 0.06},
                    {"class": "特应性皮炎", "class_en": "Atopic Dermatitis", "probability": 0.04},
                    {"class": "脂溢性皮炎", "class_en": "Seborrheic Dermatitis", "probability": 0.02},
                    {"class": "扁平苔藓", "class_en": "Lichen Planus", "probability": 0.01}
                ]
                
                st.session_state["detection_result"] = {
                    "boxes": boxes,
                    "labels": labels,
                    "confidences": confidences,
                    "image": result_image
                }
                
                st.session_state["current_diagnosis"] = {
                    "model_used": model_name,
                    "top1": top5_results[0],
                    "top5": top5_results,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "image_name": uploaded_file.name
                }
                
                st.rerun()
    
    # 重新上传按钮
    if st.session_state.get("current_diagnosis"):
        if st.button("🔄 重新上传", use_container_width=True):
            st.session_state["current_diagnosis"] = None
            st.session_state["detection_result"] = None
            st.rerun()

with col2:
    st.markdown("### 📋 诊断结果")
    
    if st.session_state.get("current_diagnosis"):
        diagnosis = st.session_state["current_diagnosis"]
        detection = st.session_state.get("detection_result")
        
        # 显示带检测框的图像
        if detection and detection.get("image"):
            st.image(detection["image"], caption="检测结果", use_container_width=True)
        
        # 检测框信息（可折叠）
        with st.expander("📍 检测框信息", expanded=False):
            if detection and detection.get("boxes"):
                for i, (box, label, conf) in enumerate(zip(
                    detection["boxes"], detection["labels"], detection["confidences"]
                )):
                    st.write(f"**区域 {i+1}:** {label}")
                    st.write(f"  - 坐标: [{box[0]}, {box[1]}, {box[2]}, {box[3]}]")
                    st.write(f"  - 置信度: {conf:.2%}")
        
        # 主要诊断结果
        top1 = diagnosis["top1"]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%); 
                    padding: 25px; border-radius: 15px; color: white; text-align: center;
                    margin: 20px 0;">
            <h2 style="margin: 0; color: white !important;">{top1['class']}</h2>
            <p style="font-size: 14px; opacity: 0.9; margin: 10px 0 0 0;">
                {top1['class_en']}
            </p>
            <h1 style="font-size: 48px; margin: 15px 0 0 0; color: white !important;">
                {top1['probability']:.1%}
            </h1>
            <p style="font-size: 12px; opacity: 0.8;">置信度</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**使用模型:** `{diagnosis['model_used']}`")
        st.markdown(f"**诊断时间:** {diagnosis['timestamp']}")
        
        # Top-5 概率列表
        st.markdown("### 📊 Top-5 概率分布")
        
        top5_data = diagnosis["top5"]
        
        # 使用Streamlit的指标条展示
        for i, item in enumerate(top5_data):
            prob = item["probability"]
            color = "#1890ff" if i == 0 else "#8c8c8c"
            
            st.markdown(f"""
            <div style="margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span><b>{i+1}. {item['class']}</b></span>
                    <span style="color: {color};">{prob:.2%}</span>
                </div>
                <div style="background: #f0f0f0; border-radius: 5px; height: 12px; overflow: hidden;">
                    <div style="background: {color}; width: {prob*100}%; height: 100%; 
                                border-radius: 5px; transition: width 0.5s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 诊断建议
        st.markdown("### 💡 诊断建议")
        
        disease_advice = {
            "银屑病": "建议到皮肤科进行专业检查。避免抓挠患处，保持皮肤湿润，减少精神压力。",
            "湿疹": "保持皮肤清洁湿润，避免接触刺激性物质。建议就医确认类型并接受治疗。",
            "特应性皮炎": "注意皮肤护理，避免过敏原。症状持续或加重时请就医。",
            "黑色素瘤": "建议尽快就医进行活检确认。黑色素瘤早期发现治愈率高。",
        }
        
        advice = disease_advice.get(top1["class"], "建议咨询专业医生获取详细诊断。")
        st.info(advice)
        
        # 操作按钮
        st.markdown("### ⚡ 操作")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("💾 保存诊断记录", use_container_width=True):
                # 保存到历史记录
                if "diagnosis_records" not in st.session_state:
                    st.session_state["diagnosis_records"] = []
                
                record = {
                    "id": len(st.session_state["diagnosis_records"]) + 1,
                    "image_name": diagnosis.get("image_name", "未知"),
                    "disease": top1["class"],
                    "confidence": top1["probability"],
                    "timestamp": diagnosis["timestamp"]
                }
                st.session_state["diagnosis_records"].append(record)
                st.success("诊断记录已保存!")
        
        with col_btn2:
            if st.button("📄 导出报告", use_container_width=True):
                report = f"""
====================================
       皮肤病诊断报告
====================================

诊断时间: {diagnosis['timestamp']}
上传图像: {diagnosis.get('image_name', '未知')}

诊断结果:
  - 疾病名称: {top1['class']} ({top1['class_en']})
  - 置信度: {top1['probability']:.2%}

Top-5 诊断列表:
"""
                for i, item in enumerate(top5_data, 1):
                    report += f"  {i}. {item['class']}: {item['probability']:.2%}\n"
                
                report += f"""
诊断建议:
{advice}

====================================
本报告仅供参考，请以医生诊断为准
====================================
"""
                st.download_button(
                    label="下载报告",
                    data=report,
                    file_name=f"诊断报告_{diagnosis['timestamp'].replace(':', '-')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    else:
        # 空状态
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px; 
                    background: #f8fafc; border-radius: 15px; border: 2px dashed #d9d9d9;">
            <p style="font-size: 48px; margin: 0;">📷</p>
            <p style="color: #666; margin: 15px 0;">请上传皮肤病变图像</p>
            <p style="color: #999; font-size: 12px;">支持 JPG、PNG 格式</p>
        </div>
        """, unsafe_allow_html=True)

# 底部说明
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 20px;">
    <p>💡 提示：本系统基于深度学习模型，仅供参考，不作为正式医疗诊断依据</p>
</div>
""", unsafe_allow_html=True)
