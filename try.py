import openai
import streamlit as st
from docx import Document
from io import BytesIO

st.title('Alfafe')
uploaded_file = st.file_uploader("Upload a Word document", type="docx")
doc = Document(uploaded_file)
for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            st.text(paragraph.text)
            st.text("-----------------------------")
            

