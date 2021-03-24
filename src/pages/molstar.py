'''Streamlit Service
Created on 21/03/21
Created by @Blastorios'''

import re
from pathlib import Path

import streamlit as st
import streamlit.components as comp

from utils import Page


class MolStar(Page):

    MOLSTAR_VIEWER = r"https://molstar.org/viewer/"

    def __init__(self, state):
        self.state = state

    def write(self):
        """Set the MolStar Viewer
        """
        molstar_width = st.sidebar.slider("MolStar Width",
                                          min_value=500, max_value=2000,
                                          value=1250, step=10,
                                          help="Set the MolStar width")

        molstar_height = st.sidebar.slider("MolStar Hieght",
                                           min_value=500, max_value=2000,
                                           value=900, step=10,
                                           help="Set the MolStar width")

        comp.v1.iframe(MolStar.MOLSTAR_VIEWER,
                       width=molstar_width, height=molstar_height)
