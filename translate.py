import openai
import streamlit as st
from docx import Document
from io import BytesIO


openai.api_key = st.secrets['my_key']

def translate_text(text, target_language="ko"):
    prompt = f"Translate the following text to {target_language}:\n\n{text}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional insurance lawyer who is good at translating documents accurately while keeping paragraphing and styles. I will myself provide the text to you, so after translating, do not reply anything other than translation. Because I will copy the translations you provided, and if you ask or say something, this might ruin the translation. And just translate as it is."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    translated_text = response.choices[0].message.content.strip()
    return translated_text

def translate_document(doc, target_language="ko"):
    translated_doc = Document()
    for paragraph in doc.paragraphs:
        translated_text = translate_text(paragraph.text, target_language)
        translated_doc.add_paragraph(translated_text)
    return translated_doc

st.title("Document Translator")


uploaded_file = st.file_uploader("Upload a Word document", type="docx")

if uploaded_file is not None:
    doc = Document(uploaded_file)
    target_language = st.selectbox("Select target language", [("Korean", "ko"), ("English", "eng")], format_func=lambda x: x[0]) 
    if st.button("Translate"):
        translated_doc = translate_document(doc, target_language)
        output = BytesIO()
        translated_doc.save(output)
        output.seek(0)
        st.download_button(
            label="Download Translated Document",
            data=output,
            file_name="translated_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ) 