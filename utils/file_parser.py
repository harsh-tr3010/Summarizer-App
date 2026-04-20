import PyPDF2
import docx

def extract_text(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

    elif file_type == "pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    elif file_type == "docx":
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    return ""