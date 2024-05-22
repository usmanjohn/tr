import openai
import streamlit as st
from docx import Document
from io import BytesIO

openai.api_key = st.secrets['my_key']

def translate_text(messages, text, target_language="ko"):
    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000
    )
    translated_text = response.choices[0].message['content'].strip()
    return translated_text, messages

def translate_document(doc, target_language="ko"):
    system_message = {
        "role": "system",
        "content": "Important: Do not never reply except translated text or 'wowo'. Reply 'wowo' if you have any problem. You are a professional insurance lawyer who is good at translating documents accurately while keeping paragraphing and styles."
    }
    messages = [system_message]

    translated_doc = Document()
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            translated_text, messages = translate_text(messages, paragraph.text, target_language)
            translated_doc.add_paragraph(translated_text)
    return translated_doc

st.title("Document Translator")

uploaded_file = st.file_uploader("Upload a Word document", type="docx")

if uploaded_file is not None:
    doc = Document(uploaded_file)
    language_options = [("Korean", "ko"), ("English", "eng"), ("French", "fr"), ("Spanish", "es"), ("German", "de"), ("Chinese", "zh")]
    target_language = st.selectbox("Select target language", language_options, format_func=lambda x: x[0])[1]
    
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
