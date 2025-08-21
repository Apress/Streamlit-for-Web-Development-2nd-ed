# Add custom footer to the sidebar
custom_footer_style = """
    <div class="markdown-text-container stText" style="width: 698px;">
        <footer>
            <p></p>
        </footer>
        <div style="font-size: 12px;">Hello world v 0.1</div>
        <div style="font-size: 12px;">Hello world LLC.</div>
    </div>
    """
st.sidebar.markdown(custom_footer_style, unsafe_allow_html=True)
