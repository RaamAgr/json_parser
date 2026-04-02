import streamlit as st
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="JSON Mastery", page_icon="🦄", layout="wide")

# Inject SEO Meta Tags separate from CSS so Streamlit markdown parser doesn't break
seo_tags = """
<meta name="description" content="A vibrant, lightning-fast, and minimal JSON parser and formatter. Parse, format, and minify your JSON data effortlessly.">
<meta name="keywords" content="JSON, parser, formatter, minify, format, online tool, developer tools, clean UI">
"""
st.markdown(seo_tags, unsafe_allow_html=True)

custom_css = """
<style>
/* Hide default structural elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Dark UI App Background */
.stApp {
    background: linear-gradient(135deg, #090e17 0%, #171d2b 100%);
    background-attachment: fixed;
    color: #e0e0e0;
}

/* The primary page container gets a sleek glassmorphic card look */
div.block-container {
    background: rgba(16, 23, 37, 0.7);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 3rem !important;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    margin-top: 2rem;
    margin-bottom: 2rem;
    max-width: 1200px;
}

/* Typography Enhancements */
h1 {
    background: -webkit-linear-gradient(45deg, #00e676, #00b0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    margin-bottom: 0.5rem !important;
}

h3 {
    color: #cfd8dc !important;
    font-weight: 500 !important;
    border-bottom: 2px solid rgba(255,255,255,0.05);
    padding-bottom: 0.5rem;
    margin-top: 1rem;
}

/* Text area styling - Glowing Focus */
div[data-baseweb="textarea"] {
    background-color: rgba(0, 0, 0, 0.4) !important;
    border: 2px solid #2d3748 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease;
}

div[data-baseweb="textarea"]:focus-within {
    border-color: #00b0ff !important;
    box-shadow: 0 0 15px rgba(0, 176, 255, 0.3) !important;
}

textarea {
    font-family: 'Fira Code', source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace !important;
    color: #8ed1fc !important;
}

/* File uploader dropzone */
section[data-testid="stFileUploadDropzone"] {
    background-color: rgba(0, 0, 0, 0.2) !important;
    border: 2px dashed #4a5568 !important;
    border-radius: 15px !important;
    transition: all 0.3s ease;
}

section[data-testid="stFileUploadDropzone"]:hover {
    border-color: #00e676 !important;
    background-color: rgba(0, 230, 118, 0.05) !important;
}

/* Remove default border/padding around forms */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Custom submit button styling (Primary Button) */
button[kind="primaryFormSubmit"], button[kind="primary"] {
    background: linear-gradient(135deg, #00e676 0%, #00b0ff 100%) !important;
    color: #1a202c !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 700 !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    margin-top: 10px;
}

button[kind="primaryFormSubmit"]:hover, button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 15px rgba(0, 230, 118, 0.3) !important;
}

/* Secondary normal buttons for utilities / downloads */
button[data-testid="stBaseButton-secondary"] {
    background: rgba(255,255,255,0.05) !important;
    color: #e0e0e0 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
    font-size: 0.9rem !important;
}

button[data-testid="stBaseButton-secondary"]:hover {
    background: rgba(255,255,255,0.1) !important;
    border-color: #00b0ff !important;
}

div.stAlert {
    border-radius: 12px;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize Session State
if "parsed_json" not in st.session_state:
    st.session_state.parsed_json = None
if "is_error" not in st.session_state:
    st.session_state.is_error = False
if "error_msg" not in st.session_state:
    st.session_state.error_msg = ""
if "raw_json_cache" not in st.session_state:
    st.session_state.raw_json_cache = ""

# Main Application Layout
st.markdown("<h1>🦄 JSON Mastery</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.1rem; color: #a0aec0; margin-bottom: 1.5rem;'>Experience JSON parsing like never before.</p>", unsafe_allow_html=True)

input_col1, input_col2 = st.columns([1, 6])
with input_col1:
    st.markdown("<div style='padding-top:0.3rem; color: #a0aec0; font-weight: 600;'>Input Mode:</div>", unsafe_allow_html=True)
with input_col2:
    input_method = st.radio("Source", ["Paste JSON", "Upload File"], horizontal=True, label_visibility="collapsed")

raw_json = ""
submit_clicked = False

st.write("")

if input_method == "Paste JSON":
    with st.form("paste_form", clear_on_submit=False):
        raw_json_input = st.text_area("JSON Code", value=st.session_state.raw_json_cache, height=300, placeholder='{\n  "status": "ready",\n  "message": "Type your JSON and hit Cmd+Enter / Ctrl+Enter or click the button below..."\n}', label_visibility="collapsed")
        # st.form intrinsically allows executing via Enter/Cmd+Enter depending on the field
        submit_clicked = st.form_submit_button("🚀 Parse & Render", type="primary", use_container_width=True)
        if submit_clicked:
            raw_json = raw_json_input
            st.session_state.raw_json_cache = raw_json
else:
    with st.form("upload_form", clear_on_submit=False):
        uploaded_file = st.file_uploader("Drop your JSON file here", type=["json"], label_visibility="collapsed")
        submit_clicked = st.form_submit_button("🚀 Parse & Render", type="primary", use_container_width=True)
        if submit_clicked and uploaded_file is not None:
            try:
                raw_json = uploaded_file.read().decode("utf-8")
                st.session_state.raw_json_cache = raw_json
            except Exception as e:
                st.error(f"Failed to read file: {e}")

# Process Parsing
if submit_clicked:
    if raw_json.strip():
        try:
            st.session_state.parsed_json = json.loads(raw_json)
            st.session_state.is_error = False
        except json.JSONDecodeError as e:
            st.session_state.parsed_json = None
            st.session_state.is_error = True
            st.session_state.error_msg = str(e)
    else:
        st.session_state.parsed_json = None
        st.session_state.is_error = False

# Render Output View (stays active safely across Streamlit reruns)
if st.session_state.is_error:
    st.error(f"🚫 Syntax Error: {st.session_state.error_msg}")
elif st.session_state.parsed_json is not None:
    st.write("")
    
    st.markdown("<div id='parsed-output-anchor'></div>", unsafe_allow_html=True)
    st.markdown("<h3>Parsed Explorer</h3>", unsafe_allow_html=True)
    
    if submit_clicked:
        components.html(
            """
            <script>
                setTimeout(function() {
                    const anchors = window.parent.document.querySelectorAll('#parsed-output-anchor');
                    if (anchors.length > 0) {
                        // Scroll top of screen to this anchor
                        anchors[anchors.length - 1].scrollIntoView({behavior: 'smooth', block: 'start'});
                    } else {
                        const elements = window.parent.document.querySelectorAll('.stJson');
                        if (elements.length > 0) {
                            elements[0].scrollIntoView({behavior: 'smooth', block: 'start'});
                        }
                    }
                }, 100);
            </script>
            """,
            height=0
        )
    
    # Utilities horizontal row right above the viewer, ensuring it's not distracting.
    util_col1, util_col2, util_col3 = st.columns([1.5, 1.5, 5])
    
    formatted_json = json.dumps(st.session_state.parsed_json, indent=2)
    minified_json = json.dumps(st.session_state.parsed_json, separators=(',', ':'))
    
    with util_col1:
        st.download_button(
            label="✨ Get Formatted (.json)",
            data=formatted_json,
            file_name="beautiful_structure.json",
            mime="application/json",
            use_container_width=True
        )
    with util_col2:
        st.download_button(
            label="📦 Get Minified (.json)",
            data=minified_json,
            file_name="compact_structure.json",
            mime="application/json",
            use_container_width=True
        )
        
    st.write("")
    
    # Deep visual focus exclusively on the JSON
    st.json(st.session_state.parsed_json, expanded=True)
    
    with st.expander("View Raw Output Code"):
        st.code(formatted_json, language="json")
