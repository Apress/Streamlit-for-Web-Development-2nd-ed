import streamlit as st
import requests

# Create an empty placeholder for progress text
progress_text = st.empty()

# Create a progress bar widget, initially at 0%
progress_bar = st.progress(0)

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(filename, "wb") as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = int(downloaded * 100 / total_size) if total_size else 0

                # Update the progress text and progress bar
                progress_text.subheader(f'Progress: {percent}%')
                progress_bar.progress(percent)

    return filename

# Download a file using requests, with the custom progress bar
download_file('file url', 'output.file')