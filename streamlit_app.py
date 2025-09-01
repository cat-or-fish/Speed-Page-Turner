import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time

st.set_page_config(layout="wide")
st.title("📖 PDF Speed Reader")

# Upload
uploaded_file = st.file_uploader("Lade eine PDF hoch", type="pdf")

# Einstellungsfeld für Sekunden pro Seite
seconds = st.number_input("Sekunden pro Seite:", min_value=1, max_value=60, value=10)

if uploaded_file:
    # PDF nur einmal im Session-State speichern
    if "doc_bytes" not in st.session_state:
        st.session_state.doc_bytes = uploaded_file.read()
        st.session_state.page_index = 0

    # PDF mit PyMuPDF öffnen
    doc = fitz.open(stream=st.session_state.doc_bytes, filetype="pdf")
    total_pages = len(doc)

    # aktuelle Seite
    page_index = st.session_state.page_index
    page = doc.load_page(page_index)

    # Seite rendern in niedriger Auflösung für flüssiges Blättern
    zoom = 0.5  # 50% der Originalgröße
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    st.image(img, use_column_width=True)

    # Auto-Weiterblättern mit st_autorefresh
    if "last_update" not in st.session_state:
        st.session_state.last_update = time.time()

    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=seconds*1000, key="page_refresh")

    # Seite hochzählen für nächste Aktualisierung
    st.session_state.page_index = (st.session_state.page_index + 1) % total_pages
