"""
用户中心页面
个人信息、账号安全、系统设置
"""

import streamlit as st

st.set_page_config(page_title="用户中心", page_icon="👤", layout="wide")

# 页面标题
st.title("👤 用户中心")
st.markdown("管理您的个人信息和诊断偏好")

# 初始化用户信息
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {
        "name": "访客用户",
        "email": "",
        "phone": "",
        "age": 25,
        "gender": "未设置",
        "skin_type": "普通",
        "allergies": "",
        "theme": "light",
        "language": "中文",
        "notifications": True,
        "auto_analyze": True,
        "save_history": True
    }

user = st.session_state["user_profile"]

# 标签页
tab1, tab2, tab3, tab4 = st.tabs(["👤 基本信息", "🔒 账号安全", "⚙️ 偏好设置", "📊 数据管理"])

# ============ 基本信息 ============
with tab1:
    st.markdown("### 基本信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_name = st.text_input("昵称", value=user.get("name", ""))
        new_email = st.text_input("邮箱", value=user.get("email", ""), placeholder="your@email.com")
        new_phone = st.text_input("电话", value=user.get("phone", ""), placeholder="138xxxxx")
    
    with col2:
        age_options = list(range(0, 121))
        new_age = st.number_input("年龄", min_value=0, max_value=120, value=user.get("age", 25))
        gender_options = ["男", "女", "其他", "未设置"]
        new_gender = st.selectbox("性别", gender_options, index=gender_options.index(user.get("gender", "未设置")))
    
    st.markdown("---")
    st.markdown("### 健康信息")
    
    col3, col4 = st.columns(2)
    
    with col3:
        skin_types = ["干性", "油性", "混合性", "敏感性", "普通"]
        new_skin_type = st.selectbox(
            "皮肤类型", 
            skin_types, 
            index=skin_types.index(user.get("skin_type", "普通")) if user.get("skin_type") in skin_types else 4
        )
    
    with col4:
        new_allergies = st.text_input("过敏史", value=user.get("allergies", ""), placeholder="如：海鲜、青霉素等")
    
    # 保存按钮
    if st.button("💾 保存修改", type="primary", use_container_width=True):
        user["name"] = new_name
        user["email"] = new_email
        user["phone"] = new_phone
        user["age"] = new_age
        user["gender"] = new_gender
        user["skin_type"] = new_skin_type
        user["allergies"] = new_allergies
        st.session_state["user_profile"] = user
        st.success("信息已保存!")
        st.balloons()

# ============ 账号安全 ============
with tab2:
    st.markdown("### 修改密码")
    
    col1, col2 = st.columns(2)
    
    with col1:
        old_password = st.text_input("当前密码", type="password")
    
    with col2:
        new_password = st.text_input("新密码", type="password")
    
    confirm_password = st.text_input("确认新密码", type="password")
    
    if st.button("🔑 修改密码", use_container_width=True):
        if new_password != confirm_password:
            st.error("两次输入的密码不一致")
        elif len(new_password) < 6:
            st.error("密码长度至少6位")
        else:
            st.success("密码修改成功!")
    
    st.markdown("---")
    
    st.markdown("### 登录方式")
    
    st.info("当前为本地模式，可切换至账号登录")
    
    col_login1, col_login2 = st.columns(2)
    
    with col_login1:
        st.markdown("**账号密码登录**")
        st.text_input("用户名/邮箱")
        st.text_input("密码", type="password")
        st.button("登录", use_container_width=True)
    
    with col_login2:
        st.markdown("**第三方登录**")
        st.button("🔵 使用微信登录", use_container_width=True)
        st.button("🟢 使用支付宝登录", use_container_width=True)

# ============ 偏好设置 ============
with tab3:
    st.markdown("### 界面设置")
    
    # 主题选择
    theme = st.radio(
        "选择主题",
        ["☀️ 浅色模式", "🌙 深色模式"],
        index=0 if user.get("theme") == "light" else 1
    )
    user["theme"] = "light" if "浅色" in theme else "dark"
    
    # 语言选择
    lang = st.radio(
        "选择语言",
        ["中文", "English"],
        index=0 if user.get("language") == "中文" else 1
    )
    user["language"] = lang
    
    st.markdown("---")
    st.markdown("### 诊断设置")
    
    # 置信度阈值
    confidence_threshold = st.slider(
        "置信度阈值",
        min_value=50,
        max_value=99,
        value=80,
        help="只显示置信度高于此值的诊断结果"
    )
    
    # 自动分析
    auto_analyze = st.checkbox("自动分析上传的图片", value=user.get("auto_analyze", True))
    user["auto_analyze"] = auto_analyze
    
    # 保存历史
    save_history = st.checkbox("自动保存诊断历史", value=user.get("save_history", True))
    user["save_history"] = save_history
    
    st.markdown("---")
    st.markdown("### 通知设置")
    
    notifications = st.toggle("启用通知", value=user.get("notifications", True))
    user["notifications"] = notifications
    
    col_notif1, col_notif2 = st.columns(2)
    
    with col_notif1:
        st.checkbox("诊断结果通知", value=True)
        st.checkbox("复诊提醒", value=True)
    
    with col_notif2:
        st.checkbox("健康资讯推送", value=False)
        st.checkbox("系统更新公告", value=True)
    
    # 保存按钮
    if st.button("⚙️ 保存偏好设置", use_container_width=True):
        st.session_state["user_profile"] = user
        st.success("偏好设置已保存!")

# ============ 数据管理 ============
with tab4:
    st.markdown("### 数据统计")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric("诊断记录", len(st.session_state.get("diagnosis_records", [])))
    
    with col_stat2:
        st.metric("对话记录", len(st.session_state.get("chat_messages", [])))
    
    with col_stat3:
        st.metric("收藏文章", 0)
    
    st.markdown("---")
    st.markdown("### 数据操作")
    
    col_data1, col_data2, col_data3 = st.columns(3)
    
    with col_data1:
        if st.button("📤 导出我的数据", use_container_width=True):
            import json
            from datetime import datetime
            
            export_data = {
                "user_profile": user,
                "diagnosis_records": st.session_state.get("diagnosis_records", []),
                "export_time": datetime.now().isoformat()
            }
            
            st.download_button(
                label="下载数据",
                data=json.dumps(export_data, ensure_ascii=False, indent=2),
                file_name=f"我的数据_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col_data2:
        if st.button("☁️ 同步到云端", use_container_width=True):
            st.info("云同步功能开发中...")
    
    with col_data3:
        if st.button("🗑️ 清空本地数据", use_container_width=True):
            st.session_state["diagnosis_records"] = []
            st.session_state["chat_messages"] = []
            st.session_state["user_profile"] = {
                "name": "访客用户",
                "email": "",
                "phone": "",
                "age": 25,
                "gender": "未设置",
                "skin_type": "普通",
                "allergies": "",
                "theme": "light",
                "language": "中文",
                "notifications": True,
                "auto_analyze": True,
                "save_history": True
            }
            st.success("本地数据已清空!")
            st.rerun()
    
    st.markdown("---")
    
    # 退出登录
    st.markdown("### 账户操作")
    
    if st.button("🚪 退出登录", type="primary", use_container_width=True):
        st.session_state["user_profile"] = {
            "name": "访客用户",
            "email": "",
            "phone": "",
            "age": 25,
            "gender": "未设置",
            "skin_type": "普通",
            "allergies": "",
            "theme": "light",
            "language": "中文",
            "notifications": True,
            "auto_analyze": True,
            "save_history": True
        }
        st.success("已退出登录")
        st.rerun()

# 底部版本信息
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 20px;">
    <p>🏥 皮肤病变AI辅助诊断系统 v2.0</p>
    <p>基于 YOLO + CNN + RAG + Agent 构建</p>
</div>
""", unsafe_allow_html=True)
