'''Streamlit Service
Created on 21/03/21
Created by @Blastorios'''

import base64
import tempfile
import time
import platform

from os import rename
from pathlib import Path
from typing import (
    Union,
    Optional,
    Tuple,
    Dict,
)

import streamlit as st
import youtube_dl as ytdl
# from PIL import Image

from utils import Page


class YouTubeDownloader(Page):
    """GameBois YouTube Downloader Service
    """

    STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / 'static'

    DOWNLOADS_PATH = (STREAMLIT_STATIC_PATH / "downloads")

    SEPARATOR = '\\' if platform.system() == 'Windows' else '/'

    def __init__(self, state) -> object:
        # Might be useful in the future
        self.base_path = Path().cwd()
        self.ytdl_filename = ""

        # system-wide applications
        self.state = state

        [folder_path.mkdir() for folder_path in [
            YouTubeDownloader.STREAMLIT_STATIC_PATH, YouTubeDownloader.DOWNLOADS_PATH,
        ] if not folder_path.is_dir()]

    def __error(self, placeholder, error_msg: str) -> None:
        """Simple helper function
        """
        placeholder.error(error_msg)
        time.sleep(2)
        placeholder.empty()

    def __check_url(self, url) -> Tuple[bool, str]:
        """So we don't get any weird, funky links
        """
        items = [
            "youtube.com",
            "youtube.no",
            "youtube.nl",
            "youtu.be"
        ]
        for check in items:
            if check in url:
                self.state.client_config["video_url"] = ""
                return True, url
        self.state.client_config["video_url"] = ""
        return False, url

    def __display_progression(self, info: Dict[str, str]) -> None:
        """Display Download Progression
        """
        self.ytdl_filename = info['filename']
        self.progress_placeholder.progress(
            int((info['downloaded_bytes']/info['total_bytes'])*100)
        )

    def __process_path(self, audio: bool, path_to_process: Union[Path, str]) -> Path:
        """
        """
        if not isinstance(path_to_process, Path):
            path_to_process = Path(path_to_process)
        old_name, old_extension = path_to_process.stem, path_to_process.suffix
        directory = path_to_process.parent
        # path_to_process.rename(
        #     Path(
        #         directory,
        #         str(old_name).strip().replace('(', '').replace(')', '').replace(" ", "")+old_extension))
        rename(path_to_process, str(directory) + YouTubeDownloader.SEPARATOR + str(old_name).strip().replace('"', '').replace("'", "").replace('(',
               '').replace(')', '').replace(" ", "")+old_extension)
        return path_to_process

    def __generate_columns(self, column_number: int = 2):
        """Generate a few streamlit columns
        """
        return st.beta_columns(column_number)

    def _make_download(self, placeholder, audio: bool = False) -> None:
        """As According to:
        https://github.com/streamlit/streamlit/issues/400
        """
        placeholder.markdown(
            f"[Download Locally]({self.__process_path(audio, self.ytdl_filename)})")

    def _get_video(self, url: str,
                   location: Union[Path, str],
                   media_type: str = 'video/mp4') -> None:
        """Download the given url through youtube-dl
        """

        # Set YDDL options appropiately
        ydl_opts = {
            # "format": f"bestvideo[ext={media_type.split('/')[-1]}]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            # "merge-output-format": f"{media_type.split('/')[-1]}",
            'outtmpl': f"",
            'verbose': True,
            'progress_hooks': [self.__display_progression]
        }

        # According to the youtube-dl docs
        ydl_opts['outtmpl'] = f"{location}/%(title)s.%(ext)s"

        # Download the requested video
        with ytdl.YoutubeDL(ydl_opts) as y_dl:
            if ydl_opts['outtmpl']:
                y_dl.download([url])
        return True

    def write(self) -> None:
        """Start writing the page content
        """
        # Set the general page functions
        st.title("YouTube Downloader")
        video_url = st.text_input("", help=f"Insert your desired YouTube url")

        # Layout for the Button and Balloon Check
        down_col, balloon_col = self.__generate_columns()
        with down_col:
            downloading = st.button("Download")
        with balloon_col:
            balloon_check = st.checkbox("Balloons")

        # Ensure we have some placeholders for our content
        notification_placeholder = st.empty()
        bar_placeholder = st.empty()

        # Remember the previous video, easier session control
        self.state.client_config["video_url"] = video_url

        # Check if the parsed URL is a legitimate YouTube link
        checked, url = self.__check_url(self.state.client_config["video_url"])

        # Initialize the downloading process if all requirements pass
        if downloading:
            if checked:
                self.downloaded = False
                self.progress_placeholder = st.empty()
                self.progress_placeholder.progress(0)
                with st.spinner('Downloading...'):
                    with tempfile.TemporaryDirectory(dir=YouTubeDownloader.DOWNLOADS_PATH) as tmpdirname:
                        try:
                            # Get the video from youtube
                            self.downloaded = self._get_video(
                                url, tmpdirname)
                        except:
                            self.__error(notification_placeholder,
                                         "Could not download the Video :cold_sweat:")

                        video_col, audio_col = self.__generate_columns()

                        if self.downloaded:
                            with video_col:
                                self._make_download(st.empty())
                            with audio_col:
                                self._make_download(st.empty())
                            # Show we are done
                            if balloon_check:
                                st.balloons()
                            self.progress_placeholder.empty()

                            # Display the video
                            if downloaded:
                                with open(self.ytdl_filename, 'rb') as video_file:
                                    st.video(video_file.read())
                                st.stop()

            else:
                if url != "":
                    st.warning(
                        "YouTube only :unamused::point_up:")
                    st.stop()
                st.stop()

        else:
            st.stop()
