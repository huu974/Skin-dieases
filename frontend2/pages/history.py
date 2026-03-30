"""
历史记录页面
诊断历史列表、详情查看
"""

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="历史记录", page_icon="📋", layout="wide")

# 页面标题
st.title("📋 诊断历史")
st.markdown("查看和管理您的历史诊断记录")

# 初始化数据
if "diagnosis_records" not in st.session_state:
    # 模拟一些历史数据
    st.session_state["diagnosis_records"] = [
        {
            "id": 1,
            "image_name": "skin_001.jpg",
            "disease": "银屑病",
            "disease_en": "Psoriasis",
            "confidence": 0.87,
            "timestamp": "2026-03-28 10:30:00"
        },
        {
            "id": 2,
            "image_name": "skin_002.jpg",
            "disease": "湿疹",
            "disease_en": "Eczema",
            "confidence": 0.76,
            "timestamp": "2026-03-27 15:20:00"
        },
        {
            "id": 3,
            "image_name": "skin_003.jpg",
            "disease": "痤疮",
            "disease_en": "Acne",
            "confidence": 0.92,
            "timestamp": "2026-03-25 09:15:00"
        }
    ]

records = st.session_state["diagnosis_records"]

# 统计信息
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("总诊断次数", len(records))

with col2:
    if records:
        dates = [r.get("timestamp", "") for r in records if r.get("timestamp")]
        last_date = dates[0] if dates else "暂无"
        st.metric("最近诊断", last_date.split()[0] if " " in last_date else last_date)
    else:
        st.metric("最近诊断", "暂无")

with col3:
    avg_confidence = sum(r.get("confidence", 0) for r in records) / len(records) if records else 0
    st.metric("平均置信度", f"{avg_confidence:.1%}")

st.markdown("---")

# 筛选和排序
col_filter, col_sort = st.columns([2, 1])

with col_filter:
    disease_filter = st.selectbox(
        "🔍 按疾病筛选",
        ["全部"] + list(set([r.get("disease", "未知") for r in records]))
    )

with col_sort:
    sort_by = st.selectbox(
        "排序方式",
        ["最新优先", "置信度最高", "最旧优先"]
    )

# 筛选数据
filtered_records = records.copy()

if disease_filter != "全部":
    filtered_records = [r for r in filtered_records if r.get("disease") == disease_filter]

if sort_by == "最新优先":
    filtered_records.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
elif sort_by == "最旧优先":
    filtered_records.sort(key=lambda x: x.get("timestamp", ""), reverse=False)
elif sort_by == "置信度最高":
    filtered_records.sort(key=lambda x: x.get("confidence", 0), reverse=True)

st.markdown(f"**共 {len(filtered_records)} 条记录**")

# 显示记录列表
if filtered_records:
    for record in filtered_records:
        disease = record.get("disease", "未知")
        disease_en = record.get("disease_en", "")
        confidence = record.get("confidence", 0)
        timestamp = record.get("timestamp", "")
        image_name = record.get("image_name", "")
        
        # 置信度颜色
        if confidence >= 0.8:
            conf_color = "#52c41a"
            conf_status = "高"
        elif confidence >= 0.6:
            conf_color = "#faad14"
            conf_status = "中"
        else:
            conf_color = "#ff4d4f"
            conf_status = "低"
        
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">
                <h3 style="margin: 0; color: #1a1a2e;">{disease}</h3>
                <p style="margin: 5px 0 0 0; color: #666; font-size: 12px;">
                    {disease_en} | {timestamp}
                </p>
                <p style="margin: 5px 0 0 0; color: #999; font-size: 12px;">
                    📷 {image_name}
                </p>
            </div>
            <div style="text-align: right;">
                <div style="background: {conf_color}; color: white; 
                            padding: 8px 16px; border-radius: 20px; font-weight: 500;">
                    {confidence:.1%} ({conf_status})
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 操作按钮
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            if st.button(f"👁️ 查看详情", key=f"view_{record['id']}", use_container_width=True):
                st.session_state["selected_record"] = record
                st.rerun()
        
        with col_btn2:
            if st.button(f"💬 咨询此病", key=f"chat_{record['id']}", use_container_width=True):
                # 跳转到对话页面并带入上下文
                st.session_state["chat_context"] = f"我之前被诊断为{disease}，想了解更多..."
                st.switch_page("pages/chat.py")
        
        with col_btn3:
            if st.button(f"🗑️ 删除", key=f"del_{record['id']}", use_container_width=True):
                st.session_state["diagnosis_records"] = [
                    r for r in st.session_state["diagnosis_records"] 
                    if r["id"] != record["id"]
                ]
                st.rerun()
        
        st.markdown("---")

else:
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; 
                background: #f8fafc; border-radius: 15px; border: 2px dashed #d9d9d9;">
        <p style="font-size: 48px; margin: 0;">📋</p>
        <p style="color: #666; margin: 15px 0;">暂无诊断记录</p>
        <p style="color: #999; font-size: 12px;">请先进行诊断分析</p>
    </div>
    """, unsafe_allow_html=True)

# 导出功能
if records:
    st.markdown("### 📥 导出数据")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        if st.button("📊 导出为CSV", use_container_width=True):
            csv_data = "ID,疾病,英文名,置信度,时间,图像名称\n"
            for r in records:
                csv_data += f"{r['id']},{r.get('disease','')},{r.get('disease_en','')},{r['confidence']:.2%},{r.get('timestamp','')},{r.get('image_name','')}\n"
            
            st.download_button(
                label="下载CSV文件",
                data=csv_data,
                file_name=f"诊断历史_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col_exp2:
        if st.button("🗑️ 清空所有记录", use_container_width=True):
            st.session_state["diagnosis_records"] = []
            st.rerun()

# 诊断趋势图
if len(records) >= 2:
    st.markdown("### 📈 诊断趋势")
    
    # 模拟趋势数据
    trend_data = {
        "日期": ["03-20", "03-22", "03-25", "03-27", "03-28"],
        "诊断数": [1, 0, 1, 1, 1]
    }
    
    st.bar_chart(trend_data.set_index("日期"))

# 底部提示
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 20px;">
    <p>💡 提示：诊断记录仅保存在本地，如需长期保存请导出</p>
</div>
""", unsafe_allow_html=True)
