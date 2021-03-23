import streamlit as st

from utils import add_custom_css
from pages import PAGE_MAP
from state import provide_state

st.set_page_config(
    page_title='GameBois Service',
    # page_icon = favicon,
    # layout='wide',
    initial_sidebar_state='auto')

add_custom_css()

st.sidebar.title("Service")
current_page = st.sidebar.radio("", sorted(list(PAGE_MAP)))


@provide_state()
def main(state=None):
    PAGE_MAP[current_page](state=state).write()


if __name__ == "__main__":
    main()
