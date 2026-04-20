import streamlit as st
from utils.file_parser import extract_text
from utils.text_cleaner import clean_text
from utils.chunker import chunk_text
from utils.summarizer import generate_summary
from utils.downloader import make_txt

st.set_page_config(
    page_title="AI Summarizer App",
    page_icon="📄",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}
.sub-title {
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 20px;
}
.card {
    padding: 22px;
    border-radius: 16px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    min-height: 420px;
}
.small-muted {
    color: #6b7280;
    font-size: 14px;
}
.word-box {
    padding: 6px 10px;
    border-radius: 10px;
    background: #eef2ff;
    display: inline-block;
    font-size: 13px;
    margin-bottom: 10px;
}
.footer-note {
    text-align:center;
    color:#6b7280;
    font-size:13px;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="main-title">📄 AI Summarizer App</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload TXT / PDF / DOCX files and generate concise summaries in English and Hindi (max 500 words each).</div>',
    unsafe_allow_html=True
)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Instructions")
    st.write("1. Upload a file")
    st.write("2. Click Generate Summary")
    st.write("3. View and download results")
    st.divider()
    st.write("Supported Formats:")
    st.write("• TXT")
    st.write("• PDF")
    st.write("• DOCX")

# ---------- Upload ----------
uploaded_file = st.file_uploader(
    "Upload your document",
    type=["txt", "pdf", "docx"]
)

# ---------- Generate ----------
if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("✨ Generate Summary", use_container_width=True):
        with st.spinner("Analyzing document and generating summaries..."):

            text = extract_text(uploaded_file)
            text = clean_text(text)

            if not text.strip():
                st.error("No readable text found in the file.")
                st.stop()

            chunks = chunk_text(text)
            combined_text = chunks[0]  # token efficient

            english, hindi = generate_summary(combined_text)

            eng_words = len(english.split())
            hin_words = len(hindi.split())

        st.divider()
        st.subheader("📌 Generated Summaries")

        col1, col2 = st.columns(2, gap="large")

        # English Card
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🇬🇧 English Summary")
            st.markdown(f'<div class="word-box">Words: {eng_words} / 500</div>', unsafe_allow_html=True)
            st.write(english)
            st.download_button(
                "⬇️ Download English Summary",
                data=make_txt(english),
                file_name="english_summary.txt",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Hindi Card
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🇮🇳 Hindi Summary")
            st.markdown(f'<div class="word-box">Words: {hin_words} / 500</div>', unsafe_allow_html=True)
            st.write(hindi)
            st.download_button(
                "⬇️ Download Hindi Summary",
                data=make_txt(hindi),
                file_name="hindi_summary.txt",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown(
    '<div class="footer-note">Built with Python + Streamlit + Groq AI</div>',
    unsafe_allow_html=True
)