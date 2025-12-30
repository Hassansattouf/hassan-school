import streamlit as st
import pandas as pd
from io import BytesIO

# إعدادات الصفحة
st.set_page_config(page_title="تطبيق الهدى", page_icon="🌟")

# محرك التحليل والمطابقة مع المنهاج السوري
def analyze_data(data_list):
    curriculum_map = {
        "مهارات علمية": ["بحث", "تجربة", "تحليل", "استنتاج", "منطق"],
        "قيم وطنية": ["سوريا", "تراث", "هوية", "مجتمع", "مسؤولية"],
        "مهارات حياتية": ["تعاون", "تواصل", "نقد", "إبداع", "حل مشكلات"]
    }
    
    analysis_results = []
    all_texts = [d['text'] for d in data_list]
    
    for entry in data_list:
        text = entry['text']
        # اكتشاف نقاط القوة بناء على المنهاج
        matched = [k for k, v in curriculum_map.items() if any(word in text for word in v)]
        
        # تحليل التقاطع (تبسيط لمفهوم النقاط المشتركة)
        common = "تنسجم مع أفكار المجموعة" if len(data_list) > 1 else "مساهمة منفردة"
        
        analysis_results.append({
            "المشارك": entry['name'],
            "المساهمة": text,
            "النقاط المشتركة": common,
            "نقاط التميز": "فريدة" if len(text) > 20 else "مختصرة",
            "مطابقة المنهاج السوري الحديث": " | ".join(matched) if matched else "عام / مهارات تواصل",
        })
    return pd.DataFrame(analysis_results)

# واجهة المستخدم
st.title("🌟 تطبيق الهدى للتحليل التربوي")
st.info("تطبيق خاص بجمع وتحليل المحادثات وفق المنهاج السوري الحديث")

if 'entries' not in st.session_state:
    st.session_state.entries = []

with st.form("input_form", clear_on_submit=True):
    name = st.text_input("اسم الطالب/المشارك")
    msg = st.text_area("نص المحادثة أو الرأي")
    add = st.form_submit_button("إضافة البيانات")
    
    if add and name and msg:
        st.session_state.entries.append({"name": name, "text": msg})
        st.success(f"تمت إضافة مساهمة {name}")

if st.session_state.entries:
    df = analyze_data(st.session_state.entries)
    st.write("### معاينة الجدول التحليلي")
    st.dataframe(df)

    # تحويل لـ Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    st.download_button(
        label="📥 تحميل جدول Excel المتوافق مع المتطلبات",
        data=output.getvalue(),
        file_name="تقرير_الهدى.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if st.button("تفريغ الذاكرة"):
    st.session_state.entries = []
    st.rerun()
