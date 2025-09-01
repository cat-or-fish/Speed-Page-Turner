import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import time

st.set_page_config(layout="wide")
st.title("📖 PDF Speed Reader")

# Upload
uploaded_file = st.file_uploader("Lade eine PDF hoch", type="pdf")

# Einstellungsfeld für Sekunden
seconds = st.number_input("Sekunden pro Seite:", min_value=1, max_value=60, value=10)

if uploaded_file:
    # PDF in Bilder umwandeln
    pages = convert_from_bytes(uploaded_file.read(), dpi=150)

    # Session-State für Seitenindex
    if "page_index" not in st.session_state:
        st.session_state.page_index = 0

    # Anzeigen der Seite
    img = pages[st.session_state.page_index]
    st.image(img, use_column_width=True)

    # Automatisch weiterblättern
    st_autorefresh = st.experimental_rerun  # Simpler "Hack"

    time.sleep(seconds)
    st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
    st.experimental_rerun()
