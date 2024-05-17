import openai
import streamlit as st
from docx import Document
from io import BytesIO
import docx


# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets['my_key']

def translate_text(text, target_language="ko"):
    prompt = f"Translate the following text to {target_language}. Only provide the translation and nothing else:\n\n{text}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional insurance lawyer who translates documents accurately while keeping the original formatting and style. Do not add any extra comments, just provide the translation."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    translated_text = response.choices[0].message.content.strip()
    return translated_text

def translate_document(doc, target_language="ko"):
    translated_doc = Document()
    
    # Translate paragraphs and tables while maintaining order
    for element in doc.element.body:
        if isinstance(element, docx.oxml.text.paragraph.CT_P):
            # Element is a paragraph
            paragraph = Document().add_paragraph()
            paragraph._element = element
            translated_text = translate_text(paragraph.text, target_language)
            translated_doc.add_paragraph(translated_text)
        elif isinstance(element, docx.oxml.table.CT_Tbl):
            # Element is a table
            table = Document().add_table(rows=0, cols=0)
            table._element = element
            new_table = translated_doc.add_table(rows=0, cols=len(table.columns))
            for row in table.rows:
                new_row = new_table.add_row()
                for idx, cell in enumerate(row.cells):
                    translated_text = translate_text(cell.text, target_language)
                    new_row.cells[idx].text = translated_text

    return translated_doc

st.title("Document Translator")

uploaded_file = st.file_uploader("Upload a Word document", type="docx")

if uploaded_file is not None:
    doc = Document(uploaded_file)
    target_language = st.selectbox("Select target language", [("Korean", "ko"), ("English", "eng")], format_func=lambda x: x[0])
    if st.button("Translate"):
        translated_doc = translate_document(doc, target_language[1])  # Use the language code for translation
        output = BytesIO()
        translated_doc.save(output)
        output.seek(0)
        st.download_button(
            label="Download Translated Document",
            data=output,
            file_name="translated_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
