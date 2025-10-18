"""
Streamlit Web Interface for Universal Code Documentation Writer.
Beautiful, Modern UI with Animations
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st  # type: ignore[import]
import tempfile
import zipfile
import io
import time

from app.core.universal_analyzer import UniversalCodeAnalyzer
from app.core.llm import DocumentationGenerator
from app.core.generators.readme_generator import READMEGenerator
from config import get_config


# Page configuration
st.set_page_config(
    page_title="AI Code Documentation Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful DARK UI and animations
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Main Background - DARK Animated Gradient */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main Container with DARK Glass Effect */
    .main .block-container {
        background: rgba(30, 30, 46, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        animation: fadeIn 0.8s ease-in;
        border: 1px solid rgba(124, 77, 255, 0.3);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Title Styling - NEON GLOW */
    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 4rem !important;
        text-align: center;
        margin-bottom: 1rem !important;
        animation: slideDown 1s ease-out;
        text-shadow: 0 0 20px rgba(124, 77, 255, 0.8), 
                     0 0 40px rgba(124, 77, 255, 0.6),
                     0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Subtitle - GLOWING */
    .subtitle {
        text-align: center;
        color: rgba(200, 200, 255, 0.95) !important;
        font-size: 1.5rem !important;
        margin-bottom: 2rem;
        animation: fadeIn 1.2s ease-in;
        font-weight: 500 !important;
        text-shadow: 0 0 10px rgba(124, 77, 255, 0.5),
                     0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* All headings in main content - LIGHT colors */
    .main h2, .main h3, .main h4 {
        color: #e0e0ff !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* All paragraph text - LIGHT for dark backgrounds */
    .main p, .main span, .main div {
        color: #b0b0d0 !important;
    }
    
    /* Labels - LIGHT and BOLD */
    .main label {
        color: #d0d0e0 !important;
        font-weight: 600 !important;
    }
    
    /* File Uploader Styling - DARK THEME */
    .stFileUploader {
        border: 3px dashed #7c4dff !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        background: rgba(124, 77, 255, 0.1) !important;
        transition: all 0.4s ease !important;
    }
    
    .stFileUploader:hover {
        border-color: #b47cff !important;
        background: rgba(124, 77, 255, 0.2) !important;
        transform: scale(1.01) !important;
        box-shadow: 0 0 30px rgba(124, 77, 255, 0.4) !important;
    }
    
    /* Upload Section Text */
    .stFileUploader label {
        color: #e0e0ff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Button Styling - NEON GLOW */
    .stButton > button {
        background: linear-gradient(135deg, #7c4dff 0%, #b47cff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.9rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(124, 77, 255, 0.5),
                    0 6px 20px rgba(0, 0, 0, 0.3) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 0 40px rgba(124, 77, 255, 0.8),
                    0 10px 30px rgba(0, 0, 0, 0.4) !important;
        background: linear-gradient(135deg, #b47cff 0%, #7c4dff 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Primary Button - CYAN GLOW */
    button[kind="primary"] {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff9d 100%) !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5),
                    0 6px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #00ff9d 0%, #00d4ff 100%) !important;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.8),
                    0 10px 30px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Metric Cards - DARK THEME with NEON */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #7c4dff 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 10px rgba(124, 77, 255, 0.6));
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0d0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stMetric {
        background: rgba(40, 40, 60, 0.8) !important;
        padding: 1.8rem !important;
        border-radius: 18px !important;
        box-shadow: 0 0 20px rgba(124, 77, 255, 0.3),
                    0 6px 20px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
        border: 1px solid rgba(124, 77, 255, 0.3) !important;
    }
    
    .stMetric:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 0 40px rgba(124, 77, 255, 0.6),
                    0 12px 35px rgba(0, 0, 0, 0.5) !important;
        border-color: rgba(124, 77, 255, 0.6) !important;
    }
    
    /* Code Block Styling - DARK */
    .stCodeBlock {
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
        animation: slideUp 0.6s ease-out;
        background: rgba(20, 20, 30, 0.9) !important;
        border: 1px solid rgba(124, 77, 255, 0.2) !important;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar Styling - DARKER */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(20, 15, 40, 0.98) 0%, rgba(30, 25, 50, 0.98) 100%) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(124, 77, 255, 0.3) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0ff !important;
    }
    
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(124, 77, 255, 0.5),
                     0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 600 !important;
    }
    
    /* Sidebar Select/Radio Options */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(124, 77, 255, 0.2) !important;
        border-color: rgba(124, 77, 255, 0.4) !important;
        color: white !important;
    }
    
    /* Progress Bar - NEON */
    .stProgress > div > div {
        background: linear-gradient(90deg, #7c4dff 0%, #00d4ff 100%) !important;
        border-radius: 10px !important;
        height: 12px !important;
        box-shadow: 0 0 15px rgba(124, 77, 255, 0.6) !important;
    }
    
    .stProgress > div {
        background: rgba(40, 40, 60, 0.5) !important;
        border-radius: 10px !important;
    }
    
    /* Success/Warning/Error Messages - DARK */
    .stSuccess {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff9d 100%) !important;
        color: #0a0a0a !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        animation: bounceIn 0.6s ease-out !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff9966 100%) !important;
        color: #0a0a0a !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.5) !important;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Expander - DARK */
    .streamlit-expanderHeader {
        background: rgba(124, 77, 255, 0.15) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        padding: 1rem 1.5rem !important;
        color: #e0e0ff !important;
        border: 1px solid rgba(124, 77, 255, 0.3) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(124, 77, 255, 0.25) !important;
        border-color: rgba(124, 77, 255, 0.5) !important;
        transform: translateX(5px);
        box-shadow: 0 0 15px rgba(124, 77, 255, 0.4) !important;
    }
    
    /* Loading Animation - NEON */
    .stSpinner > div {
        border-top-color: #7c4dff !important;
        border-width: 4px !important;
    }
    
    /* Tabs - DARK with NEON borders */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 15px !important;
        background: rgba(40, 40, 60, 0.6) !important;
        padding: 15px 30px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        border: 3px solid rgba(124, 77, 255, 0.4) !important;
        color: #b0b0d0 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 0 10px rgba(124, 77, 255, 0.2) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(124, 77, 255, 0.2) !important;
        border-color: #7c4dff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 20px rgba(124, 77, 255, 0.5) !important;
        color: #e0e0ff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c4dff 0%, #b47cff 100%) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 0 30px rgba(124, 77, 255, 0.8),
                    0 8px 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Radio Buttons - DARK */
    .stRadio > label {
        font-weight: 500;
        color: #e0e0ff !important;
    }
    
    /* Select Box - DARK */
    .stSelectbox {
        border-radius: 10px;
    }
    
    .stSelectbox > div > div {
        background: rgba(40, 40, 60, 0.8) !important;
        border-color: rgba(124, 77, 255, 0.4) !important;
        color: #e0e0ff !important;
    }
    
    /* Text Area - DARK with NEON border */
    .stTextArea textarea {
        border-radius: 15px !important;
        border: 2px solid #7c4dff !important;
        font-family: 'JetBrains Mono', monospace !important;
        background: rgba(20, 20, 30, 0.8) !important;
        color: #e0e0ff !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        box-shadow: 0 0 15px rgba(124, 77, 255, 0.2) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #b47cff !important;
        box-shadow: 0 0 30px rgba(124, 77, 255, 0.5) !important;
    }
    
    /* Download Button - CYAN GLOW */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff9d 100%) !important;
        color: #0a0a0a !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.8) !important;
    }
    
    /* Icon Animation */
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .rotating-icon {
        animation: rotate 3s linear infinite;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application entry point."""
    # Animated Header with NEON GLOW
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: white !important; font-size: 4.5rem !important; font-weight: 900 !important; 
                       text-shadow: 0 0 20px rgba(124, 77, 255, 0.8), 0 0 40px rgba(124, 77, 255, 0.6), 
                       0 0 60px rgba(124, 77, 255, 0.4), 0 4px 8px rgba(0, 0, 0, 0.5); 
                       margin-bottom: 1rem !important; animation: glow 2s ease-in-out infinite alternate;'>
                🤖 AI Code Documentation Generator
            </h1>
            <p style='color: rgba(200, 200, 255, 0.95) !important; font-size: 1.5rem !important; 
                     font-weight: 500 !important; 
                     text-shadow: 0 0 10px rgba(124, 77, 255, 0.5), 0 2px 4px rgba(0, 0, 0, 0.3);'>
                ✨ Transform your code into beautiful documentation with AI magic ✨
            </p>
        </div>
        <style>
            @keyframes glow {
                from { text-shadow: 0 0 20px rgba(124, 77, 255, 0.8), 0 0 40px rgba(124, 77, 255, 0.6); }
                to { text-shadow: 0 0 30px rgba(124, 77, 255, 1), 0 0 60px rgba(124, 77, 255, 0.8); }
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Feature highlights with DARK CARD theme
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div style='text-align: center; padding: 1.8rem; background: rgba(40, 40, 60, 0.8); 
                        border-radius: 20px; box-shadow: 0 0 20px rgba(124, 77, 255, 0.3), 0 8px 25px rgba(0, 0, 0, 0.4); 
                        transition: all 0.3s ease; border: 2px solid rgba(124, 77, 255, 0.3);'>
                <h2 style='font-size: 3.5rem; margin: 0; filter: drop-shadow(0 0 10px rgba(124, 77, 255, 0.6));'>🚀</h2>
                <p style='margin: 0.5rem 0 0 0; font-weight: 700; color: #7c4dff; font-size: 1.2rem; 
                          text-shadow: 0 0 10px rgba(124, 77, 255, 0.5);'>Fast</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 1.8rem; background: rgba(40, 40, 60, 0.8); 
                        border-radius: 20px; box-shadow: 0 0 20px rgba(0, 212, 255, 0.3), 0 8px 25px rgba(0, 0, 0, 0.4); 
                        transition: all 0.3s ease; border: 2px solid rgba(0, 212, 255, 0.3);'>
                <h2 style='font-size: 3.5rem; margin: 0; filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.6));'>🎯</h2>
                <p style='margin: 0.5rem 0 0 0; font-weight: 700; color: #00d4ff; font-size: 1.2rem;
                          text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);'>Accurate</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='text-align: center; padding: 1.8rem; background: rgba(40, 40, 60, 0.8); 
                        border-radius: 20px; box-shadow: 0 0 20px rgba(0, 255, 157, 0.3), 0 8px 25px rgba(0, 0, 0, 0.4); 
                        transition: all 0.3s ease; border: 2px solid rgba(0, 255, 157, 0.3);'>
                <h2 style='font-size: 3.5rem; margin: 0; filter: drop-shadow(0 0 10px rgba(0, 255, 157, 0.6));'>🌍</h2>
                <p style='margin: 0.5rem 0 0 0; font-weight: 700; color: #00ff9d; font-size: 1.2rem;
                          text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);'>15+ Languages</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div style='text-align: center; padding: 1.8rem; background: rgba(40, 40, 60, 0.8); 
                        border-radius: 20px; box-shadow: 0 0 20px rgba(180, 124, 255, 0.3), 0 8px 25px rgba(0, 0, 0, 0.4); 
                        transition: all 0.3s ease; border: 2px solid rgba(180, 124, 255, 0.3);'>
                <h2 style='font-size: 3.5rem; margin: 0; filter: drop-shadow(0 0 10px rgba(180, 124, 255, 0.6));'>🤖</h2>
                <p style='margin: 0.5rem 0 0 0; font-weight: 700; color: #b47cff; font-size: 1.2rem;
                          text-shadow: 0 0 10px rgba(180, 124, 255, 0.5);'>AI-Powered</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Mode selection with icons
        mode = st.selectbox(
            "Select Mode",
            ["📝 Analyze & Document Code", "📚 Generate README", "✍️ Direct Code Input"]
        )
        
        st.markdown("---")
        
        # Language filter
        config = get_config()
        all_languages = config.get_supported_languages()
        
        st.markdown("### 🌐 Supported Languages")
        # Display languages in a nice grid
        lang_html = "<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; color: white;'>"
        for lang in all_languages[:10]:
            lang_html += f"<div style='background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 5px; text-align: center;'>✓ {lang}</div>"
        lang_html += "</div>"
        st.markdown(lang_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📖 About")
        st.markdown("""
            <div style='color: white; font-size: 0.9rem;'>
            Generate comprehensive, AI-powered documentation for your code in seconds.
            Supports docstrings, JSDoc, Javadoc, and more!
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: white; font-size: 0.8rem;'>
            Made with ❤️ using AI
            </div>
        """, unsafe_allow_html=True)
    
    # Main content area based on mode
    if mode == "📝 Analyze & Document Code":
        analyze_files_mode()
    elif mode == "📚 Generate README":
        generate_readme_mode()
    elif mode == "✍️ Direct Code Input":
        direct_code_input_mode()


def analyze_files_mode():
    """File analysis mode with beautiful DARK UI."""
    st.markdown("""
        <div style='background: rgba(124, 77, 255, 0.15); padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                    box-shadow: 0 0 30px rgba(124, 77, 255, 0.4), 0 8px 30px rgba(0, 0, 0, 0.5); 
                    border: 2px solid rgba(124, 77, 255, 0.5);'>
            <h2 style='margin: 0; color: #e0e0ff; font-size: 2.8rem; font-weight: 800; text-align: center;
                       text-shadow: 0 0 15px rgba(124, 77, 255, 0.8);'>
                📁 Upload Your Code
            </h2>
            <p style='margin: 1rem 0 0 0; color: #b0b0d0; font-size: 1.2rem; text-align: center; font-weight: 500;'>
                Drop your files below and watch the AI magic happen!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # File upload with tabs - ADDED CODE INPUT TAB
    tab1, tab2, tab3 = st.tabs(["📄 Single File", "📦 Multiple Files / ZIP", "✍️ Type/Paste Code"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drop your code file here",
            type=['py', 'js', 'ts', 'jsx', 'tsx', 'java', 'cs', 'go', 'php', 'rb', 'cpp', 'c', 'h', 'rs', 'swift', 'kt'],
            help="Supports Python, JavaScript, TypeScript, Java, C#, Go, PHP, Ruby, C++, Rust, Swift, and more!",
            key="single_file_upload"
        )
        
        if uploaded_file:
            analyze_single_file(uploaded_file)
    
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        upload_type = st.radio("Choose upload type:", ["Multiple Files", "ZIP Archive"], horizontal=True)
        
        if upload_type == "Multiple Files":
            uploaded_files = st.file_uploader(
                "Drop multiple code files here",
                type=['py', 'js', 'ts', 'jsx', 'tsx', 'java', 'cs', 'go', 'php', 'rb', 'cpp', 'c', 'h', 'rs'],
                accept_multiple_files=True,
                key="multiple_files_upload"
            )
            
            if uploaded_files:
                analyze_multiple_files(uploaded_files)
        
        else:  # ZIP Archive
            uploaded_zip = st.file_uploader("Drop your ZIP archive here", type=['zip'], key="zip_upload")
            
            if uploaded_zip:
                analyze_zip_archive(uploaded_zip)
    
    with tab3:
        # CODE INPUT SECTION - NEW!
        st.markdown("""
            <div style='background: rgba(0, 212, 255, 0.1); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;
                        border: 2px solid rgba(0, 212, 255, 0.3);'>
                <h3 style='margin: 0; color: #00d4ff; text-align: center; font-size: 1.5rem;
                           text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);'>
                    💻 Type or Paste Your Code Here
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            language = st.selectbox(
                "Language",
                ["python", "javascript", "typescript", "java", "csharp", "go", "php", "ruby", "cpp", "rust"],
                index=0,
                key="code_input_language"
            )
        
        with col2:
            st.markdown(f"<p style='color: #b0b0d0; padding-top: 0.5rem;'>Selected: <span style='color: #00d4ff; font-weight: bold;'>{language.upper()}</span></p>", unsafe_allow_html=True)
        
        # Large code input area
        code_input = st.text_area(
            "Paste your code here",
            height=400,
            placeholder=f"# Paste your {language} code here...\n\ndef example_function(param1, param2):\n    \"\"\"\n    Your code will be analyzed and documented!\n    \"\"\"\n    return param1 + param2",
            label_visibility="collapsed",
            key="code_input_area"
        )
        
        if code_input:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 GENERATE DOCUMENTATION", use_container_width=True, type="primary", key="generate_from_input"):
                    # Map language to file extension
                    extension_map = {
                        'python': 'py',
                        'javascript': 'js',
                        'typescript': 'ts',
                        'java': 'java',
                        'csharp': 'cs',
                        'go': 'go',
                        'php': 'php',
                        'ruby': 'rb',
                        'cpp': 'cpp',
                        'rust': 'rs'
                    }
                    
                    file_extension = extension_map.get(language, language)
                    filename = f"snippet.{file_extension}"
                    
                    # Analyze code
                    analyzer = UniversalCodeAnalyzer()
                    
                    with st.spinner("🔍 Analyzing your code..."):
                        time.sleep(0.3)
                        result = analyzer.parse_file(filename, code_input)
                    
                    st.balloons()
                    
                    # Show analysis
                    st.markdown("<br>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("⚡ Functions", len(result.get('functions', [])))
                    with col2:
                        st.metric("🏛️ Classes", len(result.get('classes', [])))
                    with col3:
                        lines = code_input.count('\n') + 1
                        st.metric("📝 Lines", lines)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Generate documentation
                    generate_file_documentation(result, code_input, filename)


def analyze_single_file(uploaded_file):
    """Analyze a single uploaded file with animated results."""
    st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0;'>
            <h3 style='margin: 0; color: #667eea;'>📊 Analyzing: {uploaded_file.name}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Read file content
    content = uploaded_file.read().decode('utf-8')
    
    # Analyze with progress animation
    analyzer = UniversalCodeAnalyzer()
    
    with st.spinner("🔍 Analyzing your code..."):
        time.sleep(0.5)  # Brief delay for animation effect
        result = analyzer.parse_file(uploaded_file.name, content)
    
    # Animated success message
    st.balloons()
    st.success("✅ Analysis Complete!")
    
    # Display metrics with animation
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌐 Language", result.get('language', 'unknown').upper())
    
    with col2:
        st.metric("⚡ Functions", len(result.get('functions', [])))
    
    with col3:
        st.metric("🏛️ Classes", len(result.get('classes', [])))
    
    with col4:
        lines = content.count('\n') + 1
        st.metric("📝 Lines", lines)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show code preview in expandable section
    with st.expander("� Code Preview", expanded=False):
        st.code(content, language=result.get('language', 'text'), line_numbers=True)
    
    # Show extracted functions
    if result.get('functions'):
        with st.expander(f"⚡ {len(result.get('functions', []))} Functions Found", expanded=True):
            for func in result.get('functions', []):
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                                padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #667eea;'>
                        <strong>{func.get('name', 'unknown')}</strong>
                        <p style='margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;'>
                            Parameters: {len(func.get('parameters', []))} | Line: {func.get('line_number', 'N/A')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    
    # Show extracted classes
    if result.get('classes'):
        with st.expander(f"🏛️ {len(result.get('classes', []))} Classes Found", expanded=True):
            for cls in result.get('classes', []):
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(118, 75, 162, 0.05) 0%, rgba(102, 126, 234, 0.05) 100%); 
                                padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #764ba2;'>
                        <strong>{cls.get('name', 'unknown')}</strong>
                        <p style='margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;'>
                            Methods: {len(cls.get('methods', []))} | Line: {cls.get('line_number', 'N/A')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate documentation button with animation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate AI Documentation", use_container_width=True, type="primary"):
            generate_file_documentation(result, content, uploaded_file.name)


def analyze_multiple_files(uploaded_files):
    """Analyze multiple uploaded files."""
    st.subheader(f"Analyzing {len(uploaded_files)} files")
    
    analyzer = UniversalCodeAnalyzer()
    results = []
    language_stats = {}
    
    progress_bar = st.progress(0)
    
    for i, file in enumerate(uploaded_files):
        content = file.read().decode('utf-8')
        result = analyzer.parse_file(file.name, content)
        results.append(result)
        
        # Update language stats
        lang = result.get('language', 'unknown')
        language_stats[lang] = language_stats.get(lang, 0) + 1
        
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    # Display summary
    st.success(f"✅ Analyzed {len(results)} files")
    
    # Language distribution
    st.subheader("📊 Language Distribution")
    st.bar_chart(language_stats)
    
    # File details
    with st.expander("📋 File Details"):
        for result in results:
            st.markdown(f"**{result.get('file_path', 'unknown')}** - {result.get('language', 'unknown')}")


def analyze_zip_archive(uploaded_zip):
    """Analyze ZIP archive."""
    st.subheader("Analyzing ZIP Archive")
    
    # Extract ZIP to temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Extract files
        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
            zip_ref.extractall(temp_path)
        
        # Analyze repository
        analyzer = UniversalCodeAnalyzer()
        
        with st.spinner("Analyzing repository..."):
            result = analyzer.analyze_repository(str(temp_path))
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Files", result.get('total_files', 0))
        
        with col2:
            st.metric("Analyzed Files", result.get('analyzed_files', 0))
        
        with col3:
            st.metric("Languages", len(result.get('language_stats', {})))
        
        # Language statistics
        st.subheader("📊 Language Statistics")
        st.bar_chart(result.get('language_stats', {}))
        
        # Generate README button
        if st.button("Generate README"):
            generate_readme_from_analysis(result)


def generate_readme_mode():
    """README generation mode."""
    st.header("📝 Generate README")
    
    uploaded_zip = st.file_uploader(
        "Upload project ZIP archive",
        type=['zip'],
        help="Upload a ZIP archive of your project"
    )
    
    project_name = st.text_input("Project Name (optional)")
    
    if uploaded_zip:
        # Extract and analyze
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_path)
            
            # Analyze repository
            analyzer = UniversalCodeAnalyzer()
            
            with st.spinner("Analyzing repository..."):
                repo_analysis = analyzer.analyze_repository(str(temp_path))
            
            st.success("✅ Analysis complete!")
            
            # Display summary
            st.subheader("📊 Project Summary")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Files", repo_analysis.get('total_files', 0))
                st.metric("Languages", len(repo_analysis.get('language_stats', {})))
            
            with col2:
                language_stats = repo_analysis.get('language_stats', {})
                if language_stats:
                    primary_lang = max(language_stats, key=language_stats.get)
                    st.metric("Primary Language", primary_lang)
            
            # Generate README
            if st.button("🚀 Generate README"):
                with st.spinner("Generating README with AI..."):
                    readme_gen = READMEGenerator()
                    readme_content = readme_gen.generate_readme(
                        repo_analysis,
                        project_name if project_name else None
                    )
                
                st.success("✅ README generated!")
                
                # Display README
                st.subheader("📄 Generated README")
                st.markdown(readme_content)
                
                # Download button
                st.download_button(
                    label="Download README.md",
                    data=readme_content,
                    file_name="README.md",
                    mime="text/markdown"
                )


def document_element_mode():
    """Document specific code element mode."""
    st.header("📚 Document Code Element")
    
    uploaded_file = st.file_uploader(
        "Upload code file",
        type=['py', 'js', 'ts', 'java', 'cs', 'go', 'php', 'rb', 'cpp', 'rs']
    )
    
    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        
        # Analyze file
        analyzer = UniversalCodeAnalyzer()
        result = analyzer.parse_file(uploaded_file.name, content)
        
        language = result.get('language', 'unknown')
        st.info(f"Detected language: **{language}**")
        
        # Select element type
        element_type = st.radio("Element Type", ["Function", "Class"])
        
        if element_type == "Function":
            functions = result.get('functions', [])
            if functions:
                function_names = [f['name'] for f in functions]
                selected_function = st.selectbox("Select Function", function_names)
                
                if st.button("Generate Documentation"):
                    func_info = next(f for f in functions if f['name'] == selected_function)
                    generate_element_documentation(func_info, language, "function")
            else:
                st.warning("No functions found in this file")
        
        else:  # Class
            classes = result.get('classes', [])
            if classes:
                class_names = [c['name'] for c in classes]
                selected_class = st.selectbox("Select Class", class_names)
                
                if st.button("Generate Documentation"):
                    class_info = next(c for c in classes if c['name'] == selected_class)
                    generate_element_documentation(class_info, language, "class")
            else:
                st.warning("No classes found in this file")


def direct_code_input_mode():
    """Direct code input mode - paste code and get instant documentation."""
    st.markdown("""
        <div style='background: rgba(0, 212, 255, 0.15); padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                    box-shadow: 0 0 30px rgba(0, 212, 255, 0.4), 0 8px 30px rgba(0, 0, 0, 0.5); 
                    border: 2px solid rgba(0, 212, 255, 0.5);'>
            <h2 style='margin: 0; color: #e0e0ff; font-size: 2.8rem; font-weight: 800; text-align: center;
                       text-shadow: 0 0 15px rgba(0, 212, 255, 0.8);'>
                ✍️ Paste Your Code
            </h2>
            <p style='margin: 1rem 0 0 0; color: #b0b0d0; font-size: 1.2rem; text-align: center; font-weight: 500;'>
                Copy-paste your code snippet and get instant AI documentation!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Language selection
    col1, col2 = st.columns([1, 3])
    with col1:
        language = st.selectbox(
            "Select Language",
            ["python", "javascript", "typescript", "java", "csharp", "go", "php", "ruby", "cpp", "rust"],
            index=0
        )
    
    # Code input area
    st.markdown("### 💻 Paste Your Code Below:")
    code_input = st.text_area(
        "Code Input",
        height=300,
        placeholder=f"Paste your {language} code here...",
        label_visibility="collapsed"
    )
    
    if code_input:
        # Analyze button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Generate Documentation", use_container_width=True, type="primary"):
                # Analyze code
                analyzer = UniversalCodeAnalyzer()
                
                with st.spinner("🔍 Analyzing code..."):
                    time.sleep(0.3)
                    result = analyzer.parse_file(f"snippet.{language}", code_input)
                
                st.balloons()
                
                # Show analysis
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("⚡ Functions", len(result.get('functions', [])))
                with col2:
                    st.metric("🏛️ Classes", len(result.get('classes', [])))
                with col3:
                    lines = code_input.count('\n') + 1
                    st.metric("📝 Lines", lines)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Generate documentation
                generate_file_documentation(result, code_input, f"snippet.{language}")


def generate_file_documentation(file_result, content, filename="code.py"):
    """Generate documentation for entire file with beautiful UI."""
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(17, 153, 142, 0.1) 0%, rgba(56, 239, 125, 0.1) 100%); 
                    padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
            <h3 style='margin: 0; color: #11998e;'>🤖 Generating AI Documentation...</h3>
        </div>
    """, unsafe_allow_html=True)
    
    doc_gen = DocumentationGenerator()
    language = file_result.get('language', 'python')
    
    # Get all functions and classes
    functions = file_result.get('functions', [])
    classes = file_result.get('classes', [])
    
    if not functions and not classes:
        st.warning("⚠️ No functions or classes found in the code. Make sure your code is properly formatted.")
        return
    
    # Progress tracking
    total_items = len(functions) + len(classes)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    generated_docs = []
    current = 0
    
    # Generate documentation for functions
    for func in functions:
        current += 1
        status_text.markdown(f"**Documenting function `{func.get('name', 'unknown')}` ({current}/{total_items})**")
        
        func['source_code'] = content
        
        with st.spinner(f"Generating docs for {func.get('name', 'unknown')}..."):
            doc = doc_gen.generate_function_documentation(func, language)
            generated_docs.append({
                'type': 'function',
                'name': func.get('name', 'unknown'),
                'doc': doc,
                'line': func.get('line_number', 'N/A')
            })
        
        progress_bar.progress(current / total_items)
    
    # Generate documentation for classes
    for cls in classes:
        current += 1
        status_text.markdown(f"**Documenting class `{cls.get('name', 'unknown')}` ({current}/{total_items})**")
        
        cls['source_code'] = content
        
        with st.spinner(f"Generating docs for {cls.get('name', 'unknown')}..."):
            doc = doc_gen.generate_class_documentation(cls, language)
            generated_docs.append({
                'type': 'class',
                'name': cls.get('name', 'unknown'),
                'doc': doc,
                'line': cls.get('line_number', 'N/A')
            })
        
        progress_bar.progress(current / total_items)
    
    progress_bar.empty()
    status_text.empty()
    
    # Success message
    st.success(f"✅ Successfully generated documentation for {total_items} items!")
    st.balloons()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display generated documentation
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;'>
            <h2 style='margin: 0; color: #667eea;'>📚 Generated Documentation</h2>
        </div>
    """, unsafe_allow_html=True)
    
    for item in generated_docs:
        icon = "⚡" if item['type'] == 'function' else "🏛️"
        color = "#667eea" if item['type'] == 'function' else "#764ba2"
        
        with st.expander(f"{icon} {item['name']} (Line {item['line']})", expanded=True):
            st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 8px; 
                            border-left: 4px solid {color};'>
            """, unsafe_allow_html=True)
            
            st.code(item['doc'], language='text')
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Copy button for this specific doc
            st.download_button(
                label=f"📥 Download {item['name']} Documentation",
                data=item['doc'],
                file_name=f"{item['name']}_doc.txt",
                mime="text/plain",
                key=f"download_{item['name']}"
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Download all documentation
    all_docs = "\n\n" + "="*80 + "\n\n".join([
        f"# {item['name']} ({item['type'].upper()})\n\n{item['doc']}"
        for item in generated_docs
    ])
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download All Documentation",
            data=all_docs,
            file_name=f"{filename}_complete_documentation.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )


def generate_readme_from_analysis(repo_analysis):
    """Generate README from repository analysis."""
    with st.spinner("Generating README with AI..."):
        readme_gen = READMEGenerator()
        readme_content = readme_gen.generate_readme(repo_analysis)
    
    st.success("✅ README generated!")
    
    st.subheader("📄 Generated README")
    st.markdown(readme_content)
    
    # Download button
    st.download_button(
        label="Download README.md",
        data=readme_content,
        file_name="README.md",
        mime="text/markdown"
    )


def generate_element_documentation(element_info, language, element_type):
    """Generate documentation for a code element."""
    doc_gen = DocumentationGenerator()
    
    with st.spinner(f"Generating {element_type} documentation..."):
        if element_type == "function":
            doc = doc_gen.generate_function_documentation(element_info, language)
        else:  # class
            doc = doc_gen.generate_class_documentation(element_info, language)
    
    st.success("✅ Documentation generated!")
    
    st.subheader("📄 Generated Documentation")
    st.code(doc, language='markdown')
    
    # Copy button
    st.download_button(
        label="Download Documentation",
        data=doc,
        file_name=f"{element_info['name']}_doc.txt",
        mime="text/plain"
    )


if __name__ == '__main__':
    main()
