from . import utils
from .pages.home import render_home
from .utils import render_sidebar, set_page, render_footer
from ..config import SIDEBAR_ENABLED

def render():
    set_page()
    if SIDEBAR_ENABLED:
        render_sidebar()
    render_home()
    render_footer()




