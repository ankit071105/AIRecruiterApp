# resume_upload.py
import streamlit as st
import PyPDF2
import docx

def handle_resume_upload():
    st.markdown("### 📄 Upload Resume")
    
    uploaded_file = st.file_uploader(
        "Drag and drop your resume here", 
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT",
        key="resume_uploader"
    )
    
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.success(f"✅ {uploaded_file.name} uploaded successfully!")
        
        # Read file content
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        else:
            return str(uploaded_file.read(), "utf-8")
    
    return None
