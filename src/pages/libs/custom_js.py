'''Streamlit Service
Created on 21/03/21
Created by @Blastorios'''

import re
from pathlib import Path

import streamlit as st


class CustomJS(object):

    def __init__(self):
        pass

    def __attach_cjs(self, text: str, check: str = ""):
        """Attach a custom piece of CSS to the html
        """
        # Get html location
        st_html = Path(st.__path__[0]) / 'static/index.html'

        # Extract content
        with open(st_html, 'r') as html_f:
            data = html_f.read()

            # Check if a given function is already present
            if check:
                if not len(re.findall(check, data)) == 0:
                    return

            # Reformat the index.html with the new .js script
            with open(st_html, 'w') as redone_html:
                new_content = re.sub('<head>', '<head>' + text, data)
                redone_html.write(new_content)

    def __set_frame_size(self):
        """Ensure we have the optimal size for our iframe
        """

        script_ref = """
        <script type="application/javascript">

        function resizeIFrameToFitContent( iFrame ) {

            iFrame.width  = iFrame.contentWindow.document.body.scrollWidth;
            iFrame.height = iFrame.contentWindow.document.body.scrollHeight;
        }

        window.addEventListener('DOMContentLoaded', function(e) {

            var iFrame = document.getElementById( 'molframe' );
            resizeIFrameToFitContent( iFrame );

            var iframes = document.querySelectorAll("iframe");
            for( var i = 0; i < iframes.length; i++) {
                resizeIFrameToFitContent( iframes[i] );
            }
        } );

        </script>
        """
        self.__attach_cjs(script_ref)
