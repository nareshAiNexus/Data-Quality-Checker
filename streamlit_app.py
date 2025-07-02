import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

st.set_page_config(page_title="Data Quality Checker", layout="wide")
st.title("📊 Data Quality Checker using LLM 🚀")

uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("✅ File successfully uploaded!")

    st.markdown("### 🔍 Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Generate quality stats
    total_rows = len(df)
    total_columns = len(df.columns)
    duplicate_rows = df.duplicated().sum()
    missing_report = df.isnull().mean() * 100
    dtypes = df.dtypes.astype(str)

    # Show metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("🧮 Total Rows", f"{total_rows}")
    col2.metric("🧾 Total Columns", f"{total_columns}")
    col3.metric("🗂️ Duplicate Rows", f"{duplicate_rows}")

    # Expanders for details
    with st.expander("🕳️ Missing Values Report"):
        st.dataframe(missing_report.reset_index().rename(columns={"index": "Column", 0: "Missing (%)"}), use_container_width=True)

    with st.expander("📦 Column Data Types"):
        st.dataframe(dtypes.reset_index().rename(columns={"index": "Column", 0: "Type"}), use_container_width=True)

    # Build raw quality text report
    report = f"""
Total Rows: {total_rows}
Total Columns: {total_columns}
Duplicate Rows: {duplicate_rows}

Missing Values (%):
{missing_report.to_string()}

Data Types:
{dtypes.to_string()}
"""

st.markdown("""
<style>
.big-font {
    font-size: 32px !important;
    font-weight: 700;
    color: #4F46E5;
}
.centered {
    text-align: center;
}
.badge {
    background-color: #E0E7FF;
    color: #3730A3;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 14px;
    margin-right: 10px;
}
.card {
    background-color: #f9fafb;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.03);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-font centered">📊 Data Quality Checker</div>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 18px; padding-top: 10px; color: #555'>
The simplest way to inspect your dataset's health using <span class='badge'>GenAI</span> + <span class='badge'>Streamlit</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### ✨ How It Works")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='card'>
        <h4>🧾 Upload CSV</h4>
        <p>Drag & drop your `.csv` file or click to select.</p>
    </div>
    <div class='card'>
        <h4>🔍 Scan Automatically</h4>
        <p>We analyze for missing data, duplicates, and type mismatches.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='card'>
        <h4>🤖 LLM Summary</h4>
        <p>A human-readable explanation of issues and cleanup suggestions.</p>
    </div>
    <div class='card'>
        <h4>💡 Smarter Data</h4>
        <p>Take confident steps toward clean, reliable data pipelines.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### 💻 Powered By")
st.markdown("""
- 🤖 **Model**: `deepseek/deepseek-r1-0528:free` via OpenRouter
- 🧠 **Framework**: Streamlit + FastAPI
- 🔐 **Privacy**: All analysis happens in-memory (no storage)
""")

st.markdown("---")


if st.button("🧠 Summarize with LLM"):
    if report.strip() == "":
        st.error("⚠️ Report is empty. Please upload a proper CSV file.")
    else:
        with st.spinner("Generating summary with LLM..."):

            prompt = f"""
You are a data quality analyst. Summarize the following raw data quality report:

{report}

Write a human-readable summary highlighting key issues and suggesting fixes.
"""

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek/deepseek-r1-0528:free",
                "messages": [
                    {"role": "system", "content": "You are a helpful data quality analyst."},
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                try:
                    summary = response.json()["choices"][0]["message"]["content"]
                    st.success("✅ Summary generated!")
                    st.markdown("### 🧠 LLM Summary")
                    st.markdown(summary)
                except Exception as e:
                    st.error("❌ Failed to parse LLM response.")
                    st.exception(e)
            else:
                st.error("❌ Failed to fetch response from LLM")
                st.code(f"Status Code: {response.status_code}")
                st.code(f"Response: {response.text}")

else:
    st.info("📁 Please upload a CSV file to begin.")
