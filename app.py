import pandas as pd
import streamlit as st

#  Page config (mobile friendly)
st.set_page_config(page_title="Loom Allocation", layout="centered")

#  Custom CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fb;
    }
    .title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
        margin-bottom: 10px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
        border: 2px solid #4A90E2;
    }
    .stFileUploader {
        border: 2px dashed #4A90E2;
        padding: 10px;
        border-radius: 10px;
        background-color: #ffffff;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    .stCode {
        background-color: #1e1e1e;
        color: #00ffcc;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 🧵 Title
st.markdown('<div class="title">🧵 Loom Allocation Data</div>', unsafe_allow_html=True)

#  File upload
uploaded_file = st.file_uploader(" Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    my = df[['LoomNo','loomAlcNo','DcoDate','LoomAlcItemcode',
             'BheemNo','LoomalcMtrs','Issue Qty','completedqty']]

    #  Input
    value = st.text_input("🔍 Enter LoomNo to filter")

    if value:
        filtered_df = my[my['LoomNo'].astype(str) == value].sort_values(by='loomAlcNo',ascending=False).reset_index()

        filtered_df.index += 1
        codes = filtered_df['LoomAlcItemcode'].unique()[:2]

        #  Styled container
        st.markdown("### 📊 Filtered Data")
        st.dataframe(filtered_df, use_container_width=True)

        #  Code output
        st.markdown("###  Item Codes (Copy)")
        for code in codes[:2]:
            st.code(code.strip())
    

        
