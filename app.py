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
@st.cache_data
def load_data(file):
    return pd.read_excel(file)
# Store file in session state
if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file

# Use stored file if available
if "uploaded_file" in st.session_state:
    df = load_data(st.session_state.uploaded_file)

    my = df[['LoomNo','loomAlcNo','DcoDate','LoomAlcItemcode',
             'BheemNo','LoomalcMtrs','Issue Qty','completedqty']]
     my['DcoDate'] = pd.to_datetime(my['DcoDate'])

    #  Input
    # Get unique LoomNos
loom_list = sorted(my['LoomNo'].dropna().astype(int).unique())
loom_list = [str(i) for i in loom_list]

# Initialize session state
if 'index' not in st.session_state:
    st.session_state.index = 0

if 'value' not in st.session_state:
    st.session_state.value = loom_list[0]


st.markdown("### 🔍 Enter LoomNo")

col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅️ Prev"):
        if st.session_state.index > 0:
            st.session_state.index -= 1
            st.session_state.value = loom_list[st.session_state.index]

with col3:
    if st.button("Next ➡️"):
        if st.session_state.index < len(loom_list) - 1:
            st.session_state.index += 1
            st.session_state.value = loom_list[st.session_state.index]

# Text input (typing allowed)
value = st.text_input("Type LoomNo", value=st.session_state.value)
# Sync manual input with index
if value in loom_list:
    st.session_state.index = loom_list.index(value)
    st.session_state.value = value

    if value:
        filtered_df = my[my['LoomNo'].astype(str) == value].sort_values(by='DcoDate',ascending=False).reset_index()

        filtered_df.index += 1
        
        #  Styled container
        #st.markdown("### 📊 Filtered Data")
        #st.dataframe(filtered_df, use_container_width=True)

        #  Code output
        # Add selection column
st.markdown("### 📊 Filtered Data")

event = st.dataframe(
    filtered_df,
    use_container_width=True,
    on_select="rerun",
    selection_mode="single-row"
)

#st.markdown("### 📋 Selected Row Data (Copy)")

if event.selection.rows:
    row_index = event.selection.rows[0]
    row = filtered_df.iloc[row_index]

    loom_no = str(row["loomAlcNo"])
    code = str(row["LoomAlcItemcode"]).strip()

    st.markdown("#### 🧵 Loom Allocation No")
    st.code(loom_no)

    st.markdown("#### 🏷️ Item Code")
    st.code(code)

else:
    st.info("Tap a row to copy data")
