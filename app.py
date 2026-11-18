
import streamlit as st

st.set_page_config(
    page_title="BuntyAI",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 BuntyAI")
st.subheader("AI YouTube Video Clipper")

st.write("Paste your own YouTube video or livestream recording link.")

url = st.text_input(
    "YouTube Video URL",
    placeholder="Paste your video link here..."
)

clip_count = st.selectbox(
    "Number of clips",
    [5, 10]
)

caption_style = st.selectbox(
    "Caption style",
    ["MrBeast Style", "Podcast Style", "Gaming Style"]
)

if st.button("🚀 Generate Clips", use_container_width=True):
    if not url.strip():
        st.error("Please paste a video link.")
    else:
        st.info("BuntyAI interface is ready. Video processing will be added next.")

st.caption("BuntyAI • Free AI Video Clipper")
