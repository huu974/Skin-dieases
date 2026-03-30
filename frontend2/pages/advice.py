"""
预防建议页面
皮肤病预防知识、日常护理建议
"""

import streamlit as st

st.set_page_config(page_title="预防建议", page_icon="🛡️", layout="wide")

# 页面标题
st.title("🛡️ 预防建议")
st.markdown("专业皮肤病预防知识和日常护理指南")

# 搜索功能
search_query = st.text_input("🔍 搜索疾病或关键词", placeholder="输入疾病名称...")

# 预防建议数据
advice_data = {
    "银屑病": {
        "icon": "🔴",
        "预防": [
            "避免感染，尤其是链球菌感染",
            "减少精神压力，保持心情愉悦",
            "戒烟戒酒",
            "避免皮肤外伤",
            "避免过度日晒"
        ],
        "饮食": [
            "多吃新鲜蔬菜水果",
            "补充Omega-3脂肪酸（鱼类）",
            "少吃牛羊肉",
            "避免辛辣刺激性食物",
            "保持充足水分摄入"
        ],
        "护理": [
            "保持皮肤湿润",
            "使用温和的护肤品",
            "避免过热的水洗澡",
            "定期使用保湿剂",
            "不要抓挠鳞屑"
        ]
    },
    "湿疹": {
        "icon": "🔵",
        "预防": [
            "保持皮肤湿润",
            "避免接触已知过敏原",
            "穿棉质宽松衣物",
            "适度洗澡，不要过度清洁",
            "保持良好的作息"
        ],
        "饮食": [
            "避免海鲜",
            "少吃辛辣食物",
            "补充维生素C",
            "多吃富含维生素的食物",
            "记录食物日记"
        ],
        "护理": [
            "使用无刺激的保湿霜",
            "避免抓挠患处",
            "用温水洗澡",
            "保持指甲修剪短",
            "使用温和的洁面产品"
        ]
    },
    "痤疮": {
        "icon": "🟠",
        "预防": [
            "每天正确清洁面部",
            "不挤压痘痘",
            "规律作息",
            "彻底卸妆",
            "避免用手触摸面部"
        ],
        "饮食": [
            "少吃甜食",
            "避免油炸食品",
            "多喝水",
            "多吃蔬菜水果",
            "控制高GI食物摄入"
        ],
        "护理": [
            "每天清洁2次",
            "使用控油护肤品",
            "避免使用油性化妆品",
            "定期更换枕套",
            "保持头发清洁"
        ]
    },
    "荨麻疹": {
        "icon": "🟡",
        "预防": [
            "查找并记录过敏原",
            "避免冷热刺激",
            "穿着宽松衣物",
            "保持皮肤清洁",
            "避免精神紧张"
        ],
        "饮食": [
            "记录食物日记",
            "避免已知过敏食物",
            "少吃辛辣食物",
            "避免酒精",
            "补充维生素"
        ],
        "护理": [
            "冷敷缓解瘙痒",
            "避免抓挠",
            "穿着宽松衣物",
            "保持皮肤湿润",
            "备好抗组胺药物"
        ]
    },
    "黑色素瘤": {
        "icon": "⚫",
        "预防": [
            "避免过度紫外线照射",
            "使用防晒霜（SPF30+）",
            "定期检查皮肤",
            "警惕痣的变化",
            "避免 tanning bed"
        ],
        "饮食": [
            "多吃抗氧化食物",
            "补充维生素D",
            "多吃蔬菜水果",
            "减少加工食品",
            "保持健康饮食"
        ],
        "护理": [
            "ABCDE自检法则",
            "定期拍照记录痣的变化",
            "及时就医检查",
            "避免刺激痣",
            "保护皮肤免受晒伤"
        ]
    },
    "手足癣": {
        "icon": "🦶",
        "预防": [
            "保持手足干燥",
            "穿透气鞋子",
            "不与他人共用拖鞋",
            "勤换袜子",
            "公共场所注意防护"
        ],
        "饮食": [
            "均衡饮食",
            "补充维生素B",
            "增强免疫力",
            "避免辛辣食物",
            "多喝水"
        ],
        "护理": [
            "每天更换袜子",
            "保持脚部干燥",
            "使用抗真菌喷雾",
            "定期消毒鞋子",
            "避免长时间浸泡"
        ]
    }
}

# 标签页布局
tab1, tab2, tab3 = st.tabs(["📚 分类预防指南", "🏥 常见疾病预防", "📋 健康生活"])

with tab1:
    st.markdown("### 分类预防指南")
    
    categories = {
        "🌞 日常防护": [
            "避免长时间暴露在阳光下，外出使用防晒霜",
            "保持皮肤清洁，每天洗澡但避免用过热的水",
            "选择温和无刺激的护肤品和沐浴产品",
            "保持充足的睡眠，增强免疫力",
            "注意个人卫生，勤洗手"
        ],
        "🍎 饮食调理": [
            "多吃新鲜蔬菜水果，补充维生素",
            "避免辛辣、油腻、刺激性食物",
            "戒烟限酒，减少对皮肤的刺激",
            "保持充足的水分摄入",
            "均衡饮食，增强体质"
        ],
        "🏃 生活习惯": [
            "规律作息，避免熬夜",
            "适当运动，增强体质",
            "学会减压，保持心情愉悦",
            "穿着宽松透气的棉质衣物",
            "避免过度劳累"
        ],
        "🏥 定期检查": [
            "定期进行皮肤自查",
            "发现问题及时就医",
            "遵医嘱用药，不擅自停药",
            "记录皮肤变化，便于医生诊断",
            "高危人群定期体检"
        ]
    }
    
    for category, tips in categories.items():
        with st.expander(category, expanded=True):
            for i, tip in enumerate(tips, 1):
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin: 10px 0;">
                    <div style="background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%); 
                                width: 30px; height: 30px; border-radius: 50%; 
                                display: flex; align-items: center; justify-content: center;
                                color: white; font-weight: bold; flex-shrink: 0; margin-right: 15px;">
                        {i}
                    </div>
                    <div style="flex: 1; padding-top: 5px;">{tip}</div>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 常见皮肤病预防")
    
    # 搜索过滤
    if search_query:
        filtered_data = {k: v for k, v in advice_data.items() if search_query in k}
    else:
        filtered_data = advice_data
    
    # 疾病选择器
    disease_names = list(filtered_data.keys())
    selected_disease = st.selectbox("选择疾病", disease_names)
    
    if selected_disease:
        disease = filtered_data[selected_disease]
        
        st.markdown(f"## {disease['icon']} {selected_disease}")
        
        # 三列布局
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: #fff2f0; padding: 20px; border-radius: 12px; 
                        border-left: 4px solid #ff4d4f;">
                <h4 style="margin: 0 0 15px 0; color: #cf1322;">🛡️ 预防措施</h4>
            </div>
            """, unsafe_allow_html=True)
            for tip in disease["预防"]:
                st.markdown(f"- {tip}")
        
        with col2:
            st.markdown("""
            <div style="background: #f9f0ff; padding: 20px; border-radius: 12px; 
                        border-left: 4px solid #722ed1;">
                <h4 style="margin: 0 0 15px 0; color: #531dab;">🍽️ 饮食建议</h4>
            </div>
            """, unsafe_allow_html=True)
            for tip in disease["饮食"]:
                st.markdown(f"- {tip}")
        
        with col3:
            st.markdown("""
            <div style="background: #fcffe6; padding: 20px; border-radius: 12px; 
                        border-left: 4px solid #a0d911;">
                <h4 style="margin: 0 0 15px 0; color: #389e0d;">💆 日常护理</h4>
            </div>
            """, unsafe_allow_html=True)
            for tip in disease["护理"]:
                st.markdown(f"- {tip}")

with tab3:
    st.markdown("### 健康生活方式")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%); 
                padding: 20px; border-radius: 12px; color: white; margin: 20px 0;">
        <h3 style="margin: 0; color: white !important;">皮肤健康五大基石</h3>
    </div>
    """, unsafe_allow_html=True)
    
    pillars = [
        ("😴", "充足睡眠", "每天7-8小时睡眠，促进皮肤修复和再生"),
        ("💧", "适量饮水", "每天饮水2000ml，保持皮肤水分"),
        ("🏃", "适度运动", "每周3-5次运动，促进血液循环"),
        ("🥗", "均衡饮食", "摄入足够的蛋白质、维生素和矿物质"),
        ("😄", "心理平衡", "保持乐观积极的心态，减少压力")
    ]
    
    for icon, title, desc in pillars:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; 
                    margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 36px; margin-right: 20px;">{icon}</span>
                <div>
                    <h4 style="margin: 0; color: #1a1a2e;">{title}</h4>
                    <p style="margin: 5px 0 0 0; color: #666;">{desc}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 警示信号
    st.markdown("---")
    st.markdown("### ⚠️ 需要及时就医的信号")
    
    warning_signs = [
        ("🔴", "皮肤肿块快速增长"),
        ("🟤", "痣的颜色或形状发生变化"),
        ("🩸", "不明原因的持续出血"),
        ("🤕", "伤口长期不愈合"),
        ("😱", "伴随全身症状的发疹")
    ]
    
    for icon, sign in warning_signs:
        st.markdown(f"- **{icon} {sign}**")

# 底部提示
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 20px;">
    <p>💡 温馨提示：以上内容仅供参考，具体预防和治疗请咨询专业医生</p>
</div>
""", unsafe_allow_html=True)
