import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time

st.set_page_config(layout="wide")
st.title("📖 PDF Speed Reader")

# Upload
uploaded_file = st.file_uploader("Lade eine PDF hoch", type="pdf")

# Einstellungsfeld für Sekunden
seconds = st.number_input("Sekunden pro Seite:", min_value=1, max_value=60, value=10)

if uploaded_file:
    # PDF mit PyMuPDF öffnen
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    # Session-State für Seitenindex
    if "page_index" not in st.session_state:
        st.session_state.page_index = 0

    page_index = st.session_state.page_index
    page = doc.load_page(page_index)

    # Seite rendern als Bild
    pix = page.get_pixmap()
    img = Image.open(io.BytesIO(pix.tobytes("png")))

    st.image(img, use_column_width=True)

    # Timer-basiertes Weiterblättern
    if "last_update" not in st.session_state:
        st.session_state.last_update = time.time()

    if time.time() - st.session_state.last_update > seconds:
        st.session_state.page_index = (st.session_state.page_index + 1) % len(doc)
        st.session_state.last_update = time.time()
        st.experimental_rerun()
