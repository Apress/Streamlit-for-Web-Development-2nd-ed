@st.cache_resource
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()
