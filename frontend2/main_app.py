"""
皮肤病智能诊断系统 - 主入口
基于 Streamlit
医疗科技蓝白风格
"""

import streamlit as st
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import time
import uuid

# 页面配置
st.set_page_config(
    page_title="皮肤病变AI辅助诊断系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 样式配置
st.markdown("""
<style>
    :root {
        --primary-color: #1890ff;
        --secondary-color: #52c41a;
    }
    .stApp { background-color: #f8fafc; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f5ff 100%);
    }
    h1, h2, h3 { color: #1a1a2e !important; font-weight: 600 !important; }
    .stButton > button {
        background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
        color: white; border: none; border-radius: 8px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(24, 144, 255, 0.4);
    }
    [data-testid="stMetricValue"] {
        font-size: 28px; font-weight: 600; color: #1890ff;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"
if "language" not in st.session_state:
    st.session_state["language"] = "中文"
if "user_info" not in st.session_state:
    st.session_state["user_info"] = {
        "name": "访客用户", "email": "", "theme": "light", "language": "中文"
    }
if "diagnosis_records" not in st.session_state:
    st.session_state["diagnosis_records"] = [
        {"id": 1, "image_name": "skin_001.jpg", "disease": "银屑病", "disease_en": "Psoriasis", "confidence": 0.87, "timestamp": "2026-03-28 10:30:00"},
        {"id": 2, "image_name": "skin_002.jpg", "disease": "湿疹", "disease_en": "Eczema", "confidence": 0.76, "timestamp": "2026-03-27 15:20:00"},
    ]
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "assistant", "content": "🏥 您好！我是皮肤病智能诊断助手。请描述您遇到的皮肤问题？"}
    ]
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "诊断分析"
if "current_diagnosis" not in st.session_state:
    st.session_state["current_diagnosis"] = None


# ============ 页面函数 ============

def page_diagnosis():
    """诊断分析页面"""
    st.title("📊 诊断分析")
    st.markdown("上传皮肤病变图像，AI将自动进行YOLO目标检测和CNN分类")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📤 图像上传")
        model_option = st.selectbox("选择分类模型", ["EfficientNet-B3 (推荐)", "ResNet50"])
        model_name = "efficientnet_b3" if "EfficientNet" in model_option else "resnet50"
        
        uploaded_file = st.file_uploader("选择皮肤病变图像", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="原始图像", use_container_width=True)
            
            if st.button("🔍 开始诊断", type="primary", use_container_width=True):
                with st.spinner("正在分析图像..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.03)
                    
                    # 模拟结果
                    boxes = [[50, 30, 250, 230]]
                    labels = ["病变区域"]
                    confidences = [0.95]
                    
                    top5_results = [
                        {"class": "银屑病", "class_en": "Psoriasis", "probability": 0.87},
                        {"class": "湿疹", "class_en": "Eczema", "probability": 0.06},
                        {"class": "特应性皮炎", "class_en": "Atopic Dermatitis", "probability": 0.04},
                        {"class": "脂溢性皮炎", "class_en": "Seborrheic Dermatitis", "probability": 0.02},
                        {"class": "扁平苔藓", "class_en": "Lichen Planus", "probability": 0.01}
                    ]
                    
                    st.session_state["current_diagnosis"] = {
                        "model_used": model_name, "top1": top5_results[0], "top5": top5_results,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "image_name": uploaded_file.name,
                        "boxes": boxes, "labels": labels, "confidences": confidences
                    }
                    st.rerun()
    
    with col2:
        st.markdown("### 📋 诊断结果")
        
        if st.session_state.get("current_diagnosis"):
            diagnosis = st.session_state["current_diagnosis"]
            top1 = diagnosis["top1"]
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%); 
                        padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
                <h2 style="margin: 0; color: white !important;">{top1['class']}</h2>
                <p style="font-size: 14px; opacity: 0.9;">{top1['class_en']}</p>
                <h1 style="font-size: 48px; margin: 15px 0 0 0; color: white !important;">{top1['probability']:.1%}</h1>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**使用模型:** `{diagnosis['model_used']}` | **时间:** {diagnosis['timestamp']}")
            
            st.markdown("### 📊 Top-5 概率分布")
            for i, item in enumerate(diagnosis["top5"]):
                prob = item["probability"]
                color = "#1890ff" if i == 0 else "#8c8c8c"
                st.markdown(f"**{i+1}. {item['class']}** - {prob:.2%}")
                st.progress(prob)
            
            st.markdown("### 💡 诊断建议")
            st.info("建议到皮肤科进行专业检查。避免抓挠患处，保持皮肤湿润，减少精神压力。")
            
            if st.button("💾 保存诊断记录", use_container_width=True):
                record = {"id": len(st.session_state["diagnosis_records"]) + 1, **diagnosis}
                st.session_state["diagnosis_records"].append(record)
                st.success("诊断记录已保存!")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px; background: #f8fafc; border-radius: 15px; border: 2px dashed #d9d9d9;">
                <p style="font-size: 48px; margin: 0;">📷</p>
                <p style="color: #666;">请上传皮肤病变图像</p>
            </div>
            """, unsafe_allow_html=True)


def page_chat():
    """智能对话页面"""
    st.title("💬 智能对话")
    st.markdown("基于RAG知识库与大语言模型的AI医生助手")
    
    # 快捷问题
    quick_questions = ["脸上长痘痘怎么办？", "湿疹怎么护理？", "银屑病有哪些症状？", "荨麻疹怎么引起的？"]
    cols = st.columns(4)
    for i, q in enumerate(quick_questions):
        if cols[i].button(q, key=f"quick_{i}"):
            st.session_state["chat_messages"].append({"role": "user", "content": q})
            response = f"关于{q}：\n\n1. 保持清洁\n2. 避免抓挠\n3. 如有加重请就医"
            st.session_state["chat_messages"].append({"role": "assistant", "content": response})
            st.rerun()
    
    st.markdown("---")
    
    # 对话记录
    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background: #e6f7ff; padding: 12px 16px; border-radius: 12px 12px 0 12px; margin: 8px 0;">
                👤 您: {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #f6ffed; padding: 12px 16px; border-radius: 12px 12px 12px 0; margin: 8px 0;">
                🏥 AI医生: {msg['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # 输入框
    user_input = st.text_input("请描述您的皮肤问题...", key="chat_input_main")
    if st.button("发送", type="primary") and user_input:
        st.session_state["chat_messages"].append({"role": "user", "content": user_input})
        response = f"感谢您的咨询！根据您描述的：{user_input}\n\n建议：\n1. 保持患处清洁\n2. 避免刺激性护肤品\n3. 如症状持续请就医"
        st.session_state["chat_messages"].append({"role": "assistant", "content": response})
        st.rerun()
    
    if st.button("🗑️ 清空对话"):
        st.session_state["chat_messages"] = [{"role": "assistant", "content": "您好！我是皮肤病智能诊断助手。请描述您遇到的皮肤问题？"}]
        st.rerun()


def page_advice():
    """预防建议页面"""
    st.title("🛡️ 预防建议")
    st.markdown("专业皮肤病预防知识和日常护理指南")
    
    search = st.text_input("🔍 搜索疾病", placeholder="输入疾病名称...")
    
    advice_data = {
        "银屑病": {"预防": ["避免感染", "减少压力", "戒烟戒酒"], "饮食": ["多吃蔬果", "补充Omega-3"], "护理": ["保持湿润", "避免抓挠"]},
        "湿疹": {"预防": ["保持湿润", "避免过敏原"], "饮食": ["避免海鲜", "补充VC"], "护理": ["使用保湿霜", "温水洗澡"]},
        "痤疮": {"预防": ["清洁面部", "不挤压"], "饮食": ["少吃甜食", "多喝水"], "护理": ["每天清洁", "使用控油产品"]},
        "荨麻疹": {"预防": ["查找过敏原"], "饮食": ["记录食物日记"], "护理": ["冷敷缓解", "避免抓挠"]},
    }
    
    diseases = list(advice_data.keys())
    selected = st.selectbox("选择疾病", diseases if not search else [d for d in diseases if search in d])
    
    if selected:
        d = advice_data[selected]
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown("### 🛡️ 预防措施"); [st.write(f"- {x}") for x in d["预防"]]
        with col2: st.markdown("### 🍽️ 饮食建议"); [st.write(f"- {x}") for x in d["饮食"]]
        with col3: st.markdown("### 💆 日常护理"); [st.write(f"- {x}") for x in d["护理"]]


def page_history():
    """历史记录页面"""
    st.title("📋 诊断历史")
    st.markdown("查看和管理您的历史诊断记录")
    
    records = st.session_state["diagnosis_records"]
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("总诊断次数", len(records))
    with col2: st.metric("最近诊断", records[0]["timestamp"] if records else "暂无")
    with col3: st.metric("平均置信度", f"{sum(r['confidence'] for r in records)/len(records):.1%}" if records else "0%")
    
    st.markdown("---")
    
    for record in records:
        conf = record["confidence"]
        color = "#52c41a" if conf >= 0.8 else "#faad14"
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0;">{record['disease']}</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 12px;">{record['disease_en']} | {record['timestamp']}</p>
                </div>
                <div style="background: {color}; color: white; padding: 8px 16px; border-radius: 20px;">
                    {conf:.1%}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def page_profile():
    """用户中心页面"""
    st.title("👤 用户中心")
    st.markdown("管理您的个人信息和诊断偏好")
    
    user = st.session_state["user_info"]
    
    tab1, tab2, tab3 = st.tabs(["👤 基本信息", "⚙️ 偏好设置", "📊 数据管理"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("昵称", value=user.get("name", ""))
            new_email = st.text_input("邮箱", value=user.get("email", ""))
        with col2:
            new_phone = st.text_input("电话", value=user.get("phone", ""))
            new_age = st.number_input("年龄", value=user.get("age", 25), min_value=0, max_value=120)
        
        if st.button("💾 保存修改", type="primary"):
            user["name"] = new_name
            user["email"] = new_email
            user["phone"] = new_phone
            user["age"] = new_age
            st.session_state["user_info"] = user
            st.success("信息已保存!")
    
    with tab2:
        theme = st.radio("主题", ["☀️ 浅色模式", "🌙 深色模式"], index=0)
        lang = st.radio("语言", ["中文", "English"], index=0)
        if st.button("⚙️ 保存偏好"):
            st.success("偏好已保存!")
    
    with tab3:
        st.metric("诊断记录", len(st.session_state["diagnosis_records"]))
        if st.button("🗑️ 清空数据"):
            st.session_state["diagnosis_records"] = []
            st.rerun()


# ============ 侧边栏导航 ============

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #1890ff; margin: 0;">🏥 MedSkin</h2>
        <p style="color: #666; font-size: 12px;">皮肤病智能诊断</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    pages = {"诊断分析": "📊", "智能对话": "💬", "预防建议": "🛡️", "历史记录": "📋", "用户中心": "👤"}
    selected = st.radio("导航", list(pages.keys()), format_func=lambda x: f"{pages[x]} {x}", label_visibility="collapsed")
    st.session_state["current_page"] = selected
    
    st.markdown("---")
    
    with st.expander("⚙️ 设置"):
        st.selectbox("主题", ["浅色模式", "深色模式"], index=0)
        st.selectbox("语言", ["中文", "English"], index=0)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%); 
                padding: 15px; border-radius: 10px; text-align: center;">
        <p style="color: white; margin: 0;">{st.session_state['user_info']['name']}</p>
    </div>
    """, unsafe_allow_html=True)


# ============ 显示当前页面 ============

if st.session_state["current_page"] == "诊断分析":
    page_diagnosis()
elif st.session_state["current_page"] == "智能对话":
    page_chat()
elif st.session_state["current_page"] == "预防建议":
    page_advice()
elif st.session_state["current_page"] == "历史记录":
    page_history()
elif st.session_state["current_page"] == "用户中心":
    page_profile()
