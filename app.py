import streamlit as st
import yt_dlp
import subprocess
import os
import tempfile
import glob

st.set_page_config(
    page_title="BuntyAI",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 BuntyAI")
st.subheader("AI Video Clipper")
st.write("Paste a link to your own video or a video you have permission to use.")

url = st.text_input(
    "YouTube Video URL",
    placeholder="Paste your video link here..."
)

clip_count = st.selectbox("Number of clips", [3, 5, 10])
clip_length = st.selectbox("Clip length (seconds)", [20, 30, 45, 60])

if st.button("🚀 Generate Clips", use_container_width=True):

    if not url.strip():
        st.error("Please enter a video URL.")

    else:
        try:
            with st.spinner("Processing your video..."):

                folder = tempfile.mkdtemp()
                output = os.path.join(folder, "source.%(ext)s")

                options = {
                    "format": "best[ext=mp4][height<=720]/best[ext=mp4]/best",
                    "outtmpl": output,
                    "noplaylist": True,
                    "quiet": True,
                    "max_filesize": 500 * 1024 * 1024,
                    "js_runtimes": {"node": {}},
                    "extractor_args": {
                        "youtube": {
                            "player_client": ["android", "ios"],
                        }
                    },
                }

                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)

                files = glob.glob(os.path.join(folder, "source.*"))

                if not files:
                    raise Exception("Video file was not created.")

                source = files[0]
                duration = info.get("duration") or 0

                if duration < clip_length:
                    raise Exception("Video is shorter than selected clip length.")

                available = duration - clip_length
                actual_count = min(clip_count, int(duration // clip_length))

                st.success("Video downloaded! Creating clips...")

                for i in range(actual_count):

                    start = int(i * available / max(1, actual_count - 1)) if actual_count > 1 else 0

                    target = os.path.join(
                        folder,
                        f"BuntyAI_clip_{i+1}.mp4"
                    )

                    command = [
                        "ffmpeg",
                        "-y",
                        "-ss", str(start),
                        "-i", source,
                        "-t", str(clip_length),
                        "-vf",
                        "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",
                        "-c:v", "libx264",
                        "-preset", "ultrafast",
                        "-c:a", "aac",
                        "-movflags", "+faststart",
                        target
                    ]

                    subprocess.run(
                        command,
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.PIPE
                    )

                    with open(target, "rb") as video:
                        st.download_button(
                            f"⬇️ Download Clip {i+1}",
                            video.read(),
                            file_name=f"BuntyAI_clip_{i+1}.mp4",
                            mime="video/mp4",
                            key=f"clip_{i+1}"
                        )

                st.success("Your MP4 clips are ready!")

        except Exception as e:
            st.error(f"Processing error: {e}")

st.caption("BuntyAI | Free Video Clipper")
