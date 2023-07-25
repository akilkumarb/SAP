import streamlit as st
from ..config import UI_PAGE_LAYOUT, SIDEBAR_ENABLED, SIDEBAR_STATUS

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

# local_css("style.css")
# remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

# icon("search")
# selected = st.text_input("", "Search...")
# button_clicked = st.button("OK")


def render_sidebar():
    with st.sidebar:
        st.image("https://scontent.fblr4-5.fna.fbcdn.net/v/t39.30808-6/300096202_5457771904290587_583053442208506901_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=HsCz9BRruz4AX9X6yDU&_nc_ht=scontent.fblr4-5.fna&oh=00_AfCPchJIABGZ5tCzjzftcI_GeiixKtoeJClUB8m9KyhXVw&oe=63CBCB27")


def set_page():
    st.set_page_config(
        page_title='SAP Upload Excel Creator', 
        page_icon="https://corp.ezetap.com/uploads/settings/logo2.png", 
        layout=UI_PAGE_LAYOUT, 
        initial_sidebar_state=SIDEBAR_STATUS if SIDEBAR_ENABLED else "auto"
    )


import streamlit.components.v1 as components
from ..paths import CUSTOM_COMPONENTS_DIR
from ..config import VERSION_INFO
FOOTER_DIR = CUSTOM_COMPONENTS_DIR / 'footer'
html_path = str(FOOTER_DIR / "element.html")
js_path = str(FOOTER_DIR / "script.js")
css_path = str(FOOTER_DIR / "style.css")

def render_footer():
    global html_path, js_path, css_path, VERSION_INFO
    with open(css_path, 'r') as f:
        css_style = "".join([line.strip() for line in f.readlines() if line.strip()])

    js_injection_text = open(js_path).read().replace("__CUSTOM_CSS__", css_style)
    js_html = f"<script>\n{js_injection_text}\n</script>"
    html_text = open(html_path).read().replace("<< __VERSION_INFO__ >>", VERSION_INFO)

    contents = html_text + "\n" + js_html

    components.html(contents,
        height=600,
        scrolling=False,
    )
