"""
智能对话页面
基于RAG知识库与Agent的AI问诊
"""

import streamlit as st
import time
import uuid
from datetime import datetime

st.set_page_config(page_title="智能对话", page_icon="💬", layout="wide")

# 页面标题
st.title("💬 智能对话")
st.markdown("基于RAG知识库与大语言模型的AI医生助手，支持多轮对话")

# 初始化会话状态
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {
            "role": "assistant",
            "content": """🏥 您好！我是皮肤病智能诊断助手。

**我可以帮您：**
- 回答皮肤病相关问题
- 根据症状提供初步建议
- 结合图像进行辅助诊断

💡 **提示：** 您可以同时上传皮肤图片，我会结合图像和症状进行综合分析。

请描述您遇到的皮肤问题？""",
            "timestamp": datetime.now().isoformat()
        }
    ]

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())


def simulate_agent_response(user_message):
    """模拟Agent响应（实际应该调用后端API）"""
    
    # 模拟推理步骤
    reasoning_steps = [
        {
            "step": "思考",
            "content": f"用户询问：{user_message}，需要分析可能的皮肤病类型和提供建议"
        },
        {
            "step": "检索",
            "content": "正在查询RAG知识库中相关的皮肤病症状描述和医疗建议"
        },
        {
            "step": "分析",
            "content": "根据症状匹配知识库中的皮肤病类型"
        },
        {
            "step": "生成",
            "content": "综合分析结果，生成回复和建议"
        }
    ]
    
    # 根据用户问题返回不同的回复
    responses = {
        "痤疮": """关于痤疮（青春痘）：

**常见原因：**
- 皮脂分泌旺盛，毛孔堵塞
- 细菌感染（痤疮丙酸杆菌）
- 激素水平变化
- 遗传因素

**护理建议：**
1. 每天用温和的洁面产品清洁面部2次
2. 不要用手挤压痘痘，以免留下疤痕
3. 选择非致痘的护肤品
4. 规律作息，减少熬夜

**饮食建议：**
- 少吃辛辣、油腻、甜食
- 多吃蔬菜水果
- 保持充足水分摄入

⚠️ 如痘痘严重或持续不退，建议就医皮肤科。""",
        
        "湿疹": """关于湿疹：

**常见症状：**
- 皮肤红斑、丘疹
- 剧烈瘙痒
- 皮肤干燥、脱屑
- 可能伴有渗出

**护理建议：**
1. 保持皮肤湿润，使用保湿霜
2. 避免过热的水洗澡
3. 穿棉质宽松衣物
4. 避免抓挠患处

**注意事项：**
- 查找并避免可能的过敏原
- 精神压力可能加重症状

⚠️ 建议就医确诊类型并接受针对性治疗。""",
        
        "银屑病": """关于银屑病（牛皮癣）：

**典型特征：**
- 红色斑块覆盖银白色鳞屑
- 薄膜现象（刮除鳞屑后可见薄膜）
- 点状出血（刮破薄膜后可见）
- 好发于头皮、肘部、膝盖

**诱发因素：**
- 感染（尤其是链球菌感染）
- 精神压力
- 外伤
- 吸烟、饮酒

**治疗原则：**
- 目前无法根治，但可控制
- 外用药物、光疗、系统治疗
- 生物制剂（重度患者）

⚠️ 请到正规医院皮肤科就诊。""",
        
        "荨麻疹": """关于荨麻疹（风团）：

**典型特征：**
- 红色或苍白色风团
- 剧烈瘙痒
- 来去迅速（24小时内消退）
- 可伴血管性水肿

**常见诱因：**
- 食物过敏（海鲜、坚果等）
- 药物过敏
- 感染
- 物理刺激（冷、热、压力）

**急性处理：**
1. 口服抗组胺药（如氯雷他定）
2. 避免已知过敏原
3. 冷敷缓解瘙痒

⚠️ 如出现呼吸困难、喉咙肿胀，请立即就医（可能过敏性休克）！"""
    }
    
    # 检查用户消息中的关键词
    user_lower = user_message.lower()
    for keyword, response in responses.items():
        if keyword in user_message:
            return response, reasoning_steps
    
    # 默认回复
    return f"""感谢您的咨询！

根据您描述的症状：{user_message}

**一般性建议：**
1. 保持患处清洁干燥
2. 避免使用刺激性护肤品
3. 观察症状变化
4. 如有加重及时就医

💡 **提升诊断准确性：**
- 请尽可能详细描述症状（位置、持续时间、变化等）
- 上传清晰的患处图片
- 说明是否有过敏史或家族病史

⚠️ 本回答仅供参考，不作为正式医疗诊断。如症状持续或加重，请尽快就医。""", reasoning_steps


# 快捷问题
st.markdown("### 💡 常见问题")

quick_questions = [
    "脸上长痘痘怎么办？",
    "身上起湿疹怎么护理？",
    "银屑病有哪些症状？",
    "荨麻疹是怎么引起的？",
    "如何预防皮肤病？",
    "皮肤瘙痒怎么办？"
]

cols = st.columns(3)
for i, q in enumerate(quick_questions):
    if cols[i % 3].button(q, key=f"quick_{i}", use_container_width=True):
        st.session_state["chat_messages"].append({
            "role": "user",
            "content": q,
            "timestamp": datetime.now().isoformat()
        })
        
        # 模拟AI回复
        with st.spinner("AI正在思考..."):
            time.sleep(1)
            response, steps = simulate_agent_response(q)
            st.session_state["chat_messages"].append({
                "role": "assistant",
                "content": response,
                "steps": steps,
                "timestamp": datetime.now().isoformat()
            })
        st.rerun()

st.markdown("---")

# 对话区域
st.markdown("### 💬 对话记录")

# 显示对话消息
chat_container = st.container()
with chat_container:
    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                <div style="background: #e6f7ff; padding: 12px 16px; 
                            border-radius: 12px 12px 0 12px; max-width: 70%;
                            border: 1px solid #91d5ff;">
                    <p style="margin: 0; color: #1890ff; font-weight: 500;">👤 您</p>
                    <p style="margin: 5px 0 0 0;">{msg['content']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 显示推理步骤（如果有）
            show_reasoning = st.checkbox("显示推理过程", value=False, key=f"show_reasoning_{msg['timestamp']}")
            
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                <div style="background: #f6ffed; padding: 12px 16px; 
                            border-radius: 12px 12px 12px 0; max-width: 70%;
                            border: 1px solid #b7eb8f;">
                    <p style="margin: 0; color: #52c41a; font-weight: 500;">🏥 AI医生</p>
                    <div style="margin: 10px 0;">{msg['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if show_reasoning and msg.get("steps"):
                with st.expander("🧠 推理过程", expanded=True):
                    for step in msg["steps"]:
                        st.markdown(f"""
                        <div style="margin: 8px 0; padding: 10px; background: #f8f8f8; border-radius: 8px;">
                            <b>{step['step']}:</b> {step['content']}
                        </div>
                        """, unsafe_allow_html=True)

# 输入区域
st.markdown("---")

# 附加图片功能
with st.expander("📎 附加图片（辅助诊断）", expanded=False):
    chat_image = st.file_uploader("上传皮肤图片", type=["jpg", "jpeg", "png"], key="chat_upload")
    if chat_image:
        st.image(chat_image, caption="附加图片", width=200)
        st.success("图片已附加到对话中")

# 聊天输入
col_input, col_send = st.columns([5, 1])

with col_input:
    user_input = st.text_input(
        "请描述您的皮肤问题...",
        placeholder="例如：脸上长了很多红痘痘怎么办？",
        label_visibility="collapsed",
        key="chat_input"
    )

with col_send:
    send_button = st.button("发送", type="primary", use_container_width=True)

# 处理发送
if send_button and user_input.strip():
    # 添加用户消息
    st.session_state["chat_messages"].append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # 模拟AI回复
    with st.spinner("AI正在思考..."):
        time.sleep(1.5)
        response, steps = simulate_agent_response(user_input)
        st.session_state["chat_messages"].append({
            "role": "assistant",
            "content": response,
            "steps": steps,
            "timestamp": datetime.now().isoformat()
        })
    
    st.rerun()

# 底部操作
st.markdown("---")

col_clear, col_export = st.columns([1, 1])

with col_clear:
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": """🏥 对话已清空

您好！我是皮肤病智能诊断助手。请描述您遇到的皮肤问题？""",
                "timestamp": datetime.now().isoformat()
            }
        ]
        st.session_state["session_id"] = str(uuid.uuid4())
        st.rerun()

with col_export:
    if st.button("📋 导出对话", use_container_width=True):
        export_text = "皮肤病智能诊断系统 - 对话记录\n"
        export_text += "=" * 50 + "\n\n"
        
        for msg in st.session_state["chat_messages"]:
            role = "用户" if msg["role"] == "user" else "AI医生"
            export_text += f"[{msg['timestamp']}] {role}:\n{msg['content']}\n\n"
        
        st.download_button(
            label="下载对话记录",
            data=export_text,
            file_name=f"对话记录_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# 提示信息
st.markdown("""
<div style="text-align: center; color: #999; padding: 20px; margin-top: 20px;">
    <p>💡 AI助手基于RAG知识库和Agent推理，仅供参考</p>
    <p>如需正式诊断，请咨询专业皮肤科医生</p>
</div>
""", unsafe_allow_html=True)
