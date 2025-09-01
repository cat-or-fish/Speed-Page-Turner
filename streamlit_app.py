import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")
st.title("📖 PDF Speed Reader")

# Upload
uploaded_file = st.file_uploader("Lade eine PDF hoch", type="pdf")

# Sekunden pro Seite
seconds = st.number_input("Sekunden pro Seite:", min_value=1, max_value=60, value=10)

if uploaded_file:
    # PDF nur einmal im Session-State speichern
    if "doc_bytes" not in st.session_state:
        st.session_state.doc_bytes = uploaded_file.read()
        st.session_state.page_index = 0
        st.session_state.pages_img = []

        # PDF mit PyMuPDF öffnen
        doc = fitz.open(stream=st.session_state.doc_bytes, filetype="pdf")

        # Alle Seiten rendern und speichern
        zoom = 0.5  # 50% der Originalgröße für flüssiges Blättern
        mat = fitz.Matrix(zoom, zoom)
        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            st.session_state.pages_img.append(img)

    total_pages = len(st.session_state.pages_img)
    page_index = st.session_state.page_index

    # Seite anzeigen
    st.image(st.session_state.pages_img[page_index], use_container_width=True)

    # Auto-Refresh
    st_autorefresh(interval=seconds*1000, key="page_refresh")

    # Index für nächste Seite erhöhen
    st.session_state.page_index = (st.session_state.page_index + 1) % total_pages
