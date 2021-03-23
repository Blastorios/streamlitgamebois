import streamlit as st
from pytube import YouTube

from utils import Page


class Testing(Page):
    def __init__(self, state):
        self.state = state

    def write(self):
        st.title("Youtube Video Downloader")
        url = st.text_input(label='URL')

        plaing = st.empty()

        if url != '':
            plaing.markdown(f"[My File]({'downloads/hehehehe'})")
