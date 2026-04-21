import streamlit as st
from utils.file_parser import extract_text
from utils.text_cleaner import clean_text
from utils.chunker import chunk_text
from utils.summarizer import generate_summary
from utils.downloader import make_txt

st.set_page_config(
    page_title="Summarizer App",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
}

.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 0;
}

.sub-title {
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 20px;
}

.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.04);
}

.metric-box {
    background: #eef2ff;
    padding: 6px 10px;
    border-radius: 8px;
    display: inline-block;
    font-size: 13px;
    margin-bottom: 10px;
    color: #3730a3;
    font-weight: 600;
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 13px;
    margin-top: 25px;
}

.stButton > button {
    background: linear-gradient(90deg,#4f46e5,#7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1rem;
    font-weight: 700;
}

.stDownloadButton > button {
    border-radius: 8px;
    font-weight: 600;
}

.summary-heading {
    margin-top: 8px;
    margin-bottom: 12px;
    font-size: 24px;
    font-weight: 700;
}

div[data-testid="stVerticalBlock"] > div:has(.card) {
    margin-top: 0 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Summarizer App</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload TXT, PDF, DOCX, PPTX or image files and generate bilingual summaries in English and Hindi (300 to 500 words).</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("How It Works")
    st.write("1. Upload your file")
    st.write("2. Click Generate Summary")
    st.write("3. View English and Hindi summaries")
    st.write("4. Download results")

    st.divider()

    st.subheader("Supported Formats")
    st.write("TXT Documents")
    st.write("PDF Files")
    st.write("DOCX Files")
    st.write("PPTX Presentations")
    st.write("PNG Images")
    st.write("JPG Images")
    st.write("JPEG Images")

    st.divider()

    st.subheader("Summary Rules")
    st.write("AI generated")
    st.write("Precise and informative")
    st.write("300 to 500 words")
    st.write("Bilingual output")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["txt", "pdf", "docx", "pptx", "png", "jpg", "jpeg"]
)

if uploaded_file:

    st.success(f"Uploaded Successfully: {uploaded_file.name}")

    if st.button("Generate Summary", use_container_width=True):

        with st.spinner("Reading file and generating summaries..."):

            text = extract_text(uploaded_file)
            text = clean_text(text)

            if not text.strip():
                st.error("No readable text found in the uploaded file.")
                st.stop()

            chunks = chunk_text(text)
            combined_text = chunks[0]

            english, hindi = generate_summary(combined_text)

            eng_words = len(english.split())
            hin_words = len(hindi.split())

        st.markdown('<div class="summary-heading">Generated Summaries</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("English Summary")
            st.markdown(
                f'<div class="metric-box">Words: {eng_words} / 500</div>',
                unsafe_allow_html=True
            )
            st.write(english)

            st.download_button(
                label="Download English Summary",
                data=make_txt(english),
                file_name="english_summary.txt",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Hindi Summary")
            st.markdown(
                f'<div class="metric-box">Words: {hin_words} / 500</div>',
                unsafe_allow_html=True
            )
            st.write(hindi)

            st.download_button(
                label="Download Hindi Summary",
                data=make_txt(hindi),
                file_name="hindi_summary.txt",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer">Built with Python, Streamlit and Groq</div>',
    unsafe_allow_html=True
)