import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import requests

# Page Configuration
st.set_page_config(
    page_title="Trading Strategy Dashboard",
    layout="wide",
    page_icon="📊"
)

# GitHub Configuration - ⚠️ CHANGE THIS TO YOUR USERNAME!
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME_HERE"  # ⚠️ CHANGE THIS LINE!
GITHUB_REPO = f"{GITHUB_USERNAME}/trading-strategy-dashboard"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/"

# CSS Styling
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; }
    .positive { color: green; font-weight: bold; }
    .negative { color: red; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# GitHub Badge
st.markdown(f"""
<a href="https://github.com/{GITHUB_USERNAME}" target="_blank" style="
    background: #24292f; color: white; padding: 8px 16px; 
    border-radius: 6px; text-decoration: none; display: inline-block;">
    <img src="https://github.githubassets.com/favicons/favicon.png" width="16" style="margin-right: 8px;">
    View on GitHub
</a>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📊 Trading Strategy Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Settings")

# Data Source Selection
data_source = st.sidebar.radio(
    "📂 Data Source",
    ["GitHub Repository", "Upload CSV", "Sample Data"]
)

# Function to load from GitHub
def load_from_github(url):
    try:
        df = pd.read_csv(url)
        return df
    except:
        return pd.DataFrame()

# Process based on selection
if data_source == "GitHub Repository":
    st.sidebar.subheader("🌐 GitHub Files")
    
    # GitHub URLs
    github_urls = {
        "Short Term Strategy": f"{GITHUB_RAW_BASE}optimizer_st.csv",
        "Long Term Strategy": f"{GITHUB_RAW_BASE}optimizer_lt.csv",
        "Sample Portfolio": f"{GITHUB_RAW_BASE}sample_portfolio.csv"
    }
    
    selected = st.sidebar.selectbox("Select File", list(github_urls.keys()))
    
    with st.spinner(f"📥 Loading from GitHub..."):
        df = load_from_github(github_urls[selected])
    
    if df.empty:
        st.error("❌ Could not load from GitHub. Please check if files exist.")
        st.info(f"Try uploading files to: https://github.com/{GITHUB_USERNAME}/trading-strategy-dashboard")
        
        # Show sample data
        sample_data = {
            "STRATEGY": ["Sample"],
            "ENTRY DATE": ["2024-01-15"],
            "SCRIP": ["RELIANCE.NS"],
            "QTY": [100],
            "ENTRY PRICE": [2500.50]
        }
        df = pd.DataFrame(sample_data)

elif data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("📤 Upload CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("📤 Please upload a CSV file")
        st.stop()
else:
    # Sample Data
    sample_data = {
        "STRATEGY": ["Momentum", "Value", "Growth"],
        "ENTRY DATE": ["2024-01-15", "2024-01-16", "2024-01-17"],
        "SCRIP": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"],
        "QTY": [100, 50, 75],
        "ENTRY PRICE": [2500.50, 3800.75, 1650.00]
    }
    df = pd.DataFrame(sample_data)

# Show Data
if not df.empty:
    st.subheader("📋 Portfolio Data")
    st.dataframe(df, use_container_width=True)
    
    # Basic Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Trades", len(df))
    with col2:
        st.metric("Total Quantity", df["QTY"].sum())
    with col3:
        st.metric("Total Investment", f"₹{(df['QTY'] * df['ENTRY PRICE']).sum():,.2f}")
    
    # GitHub Instructions Tab
    tab1, tab2 = st.tabs(["📊 Dashboard", "📖 GitHub Guide"])
    
    with tab2:
        st.subheader("📖 Complete GitHub Setup Guide")
        
        st.markdown(f"""
        ### Your GitHub Details:
        - **Username:** `{GITHUB_USERNAME}`
        - **Repository:** `trading-strategy-dashboard`
        - **Repository URL:** https://github.com/{GITHUB_USERNAME}/trading-strategy-dashboard
        
        ### 📋 Step-by-Step Guide:
        
        1. **Upload CSV Files to GitHub:**
           - Go to your repository: https://github.com/{GITHUB_USERNAME}/trading-strategy-dashboard
           - Click **"Add file"** → **"Upload files"**
           - Upload these 3 files:
             1. `optimizer_st.csv` (Short Term Strategy)
             2. `optimizer_lt.csv` (Long Term Strategy)
             3. `sample_portfolio.csv` (Sample Data)
        
        2. **Get Raw GitHub URLs:**
           - After uploading, click on a CSV file
           - Click the **"Raw"** button (top right of file content)
           - Copy the URL from address bar
           - Format: `https://raw.githubusercontent.com/{GITHUB_USERNAME}/trading-strategy-dashboard/main/optimizer_st.csv`
        
        3. **Update the App:**
           - In `app.py`, change line 16:
           ```python
           GITHUB_USERNAME = "{GITHUB_USERNAME}"  # Your actual username
           ```
        
        4. **Deploy on Streamlit Cloud:**
           - Go to [share.streamlit.io](https://share.streamlit.io)
           - Click **"New app"**
           - Select your repository
           - Click **"Deploy"**
        """)
        
        # Create sample CSV files
        st.subheader("📝 Create Sample CSV Files")
        
        if st.button("Generate Sample CSV Files"):
            # Sample data for short term
            st_data = {
                "STRATEGY": ["Momentum", "Swing"],
                "ENTRY DATE": ["2024-01-15", "2024-01-16"],
                "EXIT DATE": ["", "2024-01-20"],
                "SCRIP": ["RELIANCE.NS", "TCS.NS"],
                "QTY": [100, 50],
                "ENTRY PRICE": [2500.50, 3800.75],
                "EXIT PRICE": [None, 3850.25]
            }
            
            st_df = pd.DataFrame(st_data)
            csv_st = st_df.to_csv(index=False)
            
            st.download_button(
                label="📥 Download optimizer_st.csv",
                data=csv_st,
                file_name="optimizer_st.csv",
                mime="text/csv"
            )
            
            st.success("Download this file and upload to GitHub!")
        
        # Show GitHub URLs
        st.subheader("🔗 Your GitHub URLs")
        
        urls = [
            ("Short Term Strategy", f"{GITHUB_RAW_BASE}optimizer_st.csv"),
            ("Long Term Strategy", f"{GITHUB_RAW_BASE}optimizer_lt.csv"),
            ("Sample Portfolio", f"{GITHUB_RAW_BASE}sample_portfolio.csv")
        ]
        
        for name, url in urls:
            st.code(url, language="text")

else:
    st.warning("⚠️ No data available")

# Footer
st.markdown("---")
st.caption(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption(f"🌐 GitHub: https://github.com/{GITHUB_USERNAME}")
