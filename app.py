import streamlit as st
from utils.file_parser import extract_text
from utils.text_cleaner import clean_text
from utils.chunker import chunk_text
from utils.summarizer import generate_summary
from utils.downloader import make_txt


st.set_page_config(
    page_title="AI Document Summarizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 44px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 0px;
}

.sub-title {
    color: #6b7280;
    font-size: 17px;
    margin-bottom: 25px;
}

.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    min-height: 520px;
}

.metric-box {
    background: #eef2ff;
    padding: 7px 12px;
    border-radius: 10px;
    display: inline-block;
    font-size: 13px;
    margin-bottom: 12px;
    color: #3730a3;
    font-weight: 600;
}

.footer {
    text-align:center;
    color:#6b7280;
    font-size:13px;
    margin-top:40px;
}

.upload-box {
    padding: 10px;
    border-radius: 12px;
}

.stButton>button {
    background: linear-gradient(90deg,#4f46e5,#7c3aed);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    font-weight: 700;
}

.stDownloadButton>button {
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">AI Document Summarizer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload TXT, PDF, or DOCX files and generate precise bilingual summaries in English and Hindi (300–500 words each).</div>',
    unsafe_allow_html=True
)


with st.sidebar:
    st.header("How It Works")
    st.write("1. Upload your file")
    st.write("2. Click Generate Summary")
    st.write("3. View English & Hindi output")
    st.write("4. Download summaries")
    
    st.divider()
    
    st.subheader("Supported Formats")
    st.write("• TXT Documents")
    st.write("• PDF Files")
    st.write("• DOCX Files")
    st.write("• PPTX Presentations")
    st.write("• PNG Images")
    st.write("• JPG Images")
    st.write("• JPEG Images")

    st.divider()

    st.subheader("Summary Rules")
    st.write("• AI generated")
    st.write("• Precise & informative")
    st.write("• 300 to 500 words")
    st.write("• Bilingual output")


uploaded_file = st.file_uploader(
    "Upload Document",
    type=["txt","pdf","docx","pptx","png","jpg","jpeg"]
)


if uploaded_file:

    st.success(f"Uploaded Successfully: {uploaded_file.name}")

    if st.button("Generate Summary", use_container_width=True):

        with st.spinner("Reading document carefully and generating summaries..."):

            text = extract_text(uploaded_file)
            text = clean_text(text)

            if not text.strip():
                st.error("No readable text found in the file.")
                st.stop()

            chunks = chunk_text(text)

            
            combined_text = chunks[0]

            english, hindi = generate_summary(combined_text)

            eng_words = len(english.split())
            hin_words = len(hindi.split())

        st.divider()
        st.subheader("Generated Summaries")

        

        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🇬🇧 English Summary")
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
            st.subheader("🇮🇳 Hindi Summary")
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
    '<div class="footer">Built with Python • Streamlit • Groq AI</div>',
    unsafe_allow_html=True
)