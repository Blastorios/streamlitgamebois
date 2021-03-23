import streamlit as st
from pytube import YouTube

from utils import Page


class Testing(Page):
    def __init__(self, state):
        self.state = state

    def write(self):
        st.title("Youtube Video Downloader")
        url = st.text_input(label='URL')

        playing = st.empty()

        if url != '':
            playing.success(f"[My File]({'downloa/profi_dis_new.mp4'})")
