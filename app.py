
import streamlit as st
import yt_dlp
import imageio_ffmpeg
import subprocess
import os
import tempfile
import glob

st.set_page_config(page_title="BuntyAI", page_icon="🎬")

st.title("🎬 BuntyAI")
st.subheader("AI Video Clipper")

st.write("Paste a link to a video you own or have permission to use.")

url = st.text_input("Video URL")
clip_count = st.selectbox("Number of clips", [3, 5, 10])
clip_length = st.selectbox("Clip length", [20, 30, 45, 60])

if st.button("🚀 Generate Clips"):
    if not url.strip():
        st.error("Please enter a video URL.")
    else:
        try:
            with st.spinner("Downloading your authorized video..."):
                folder = tempfile.mkdtemp()
                output = os.path.join(folder, "source.%(ext)s")

                options = {
                    "format": "best[ext=mp4]/best",
                    "outtmpl": output,
                    "noplaylist": True,
                    "quiet": True,
                    "max_filesize": 500 * 1024 * 1024,
                }

                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)

                files = glob.glob(os.path.join(folder, "source.*"))
                if not files:
                    raise Exception("Video download failed.")

                source = files[0]
                duration = info.get("duration", 0)

            if duration < clip_length:
                raise Exception("Video is shorter than selected clip length.")

            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
            available = duration - clip_length
            step = max(1, available // clip_count)

            st.success("Video downloaded. Creating clips...")

            for i in range(clip_count):
                start = min(i * step, available)
                target = os.path.join(folder, f"BuntyAI_clip_{i+1}.mp4")

                command = [
                    ffmpeg, "-y", "-ss", str(start),
                    "-i", source, "-t", str(clip_length),
                    "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",
                    "-c:v", "libx264", "-preset", "ultrafast",
                    "-c:a", "aac", "-movflags", "+faststart", target
                ]

                subprocess.run(
                    command, check=True,
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

            st.success("Your clips are ready!")

        except Exception as e:
            st.error(f"Processing error: {e}")

st.caption("BuntyAI | Free Video Clipper")
