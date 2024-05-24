import openai
import streamlit as st
from docx import Document
from io import BytesIO


# Read the glossary file once
glossary_file_path = "glossaries.txt"

def read_glossary(file_path):
    glossary = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    term, translation = line.split('-', 1)  # Use 1 to ensure splitting only at the first hyphen
                    glossary[term.strip()] = translation.strip()
    except UnicodeDecodeError:
        st.error("Glossary file contains invalid characters. Please ensure it is UTF-8 encoded.")
    except Exception as e:
        st.error(f"An error occurred while reading the glossary file: {e}")
    return glossary

glossary = read_glossary(glossary_file_path)

st.text(glossary)