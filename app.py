
import streamlit as st
import io
import sys
import time
import traceback
from gemini_helper import call_gemini

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Python Terminal & Debugger",
    page_icon="🐍",
    layout="wide"
)

# --------------------------------------------------
# PROFESSIONAL UI STYLES
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
}

.block-container {
    background-color: #ffffffee;
    padding: 2rem;
    border-radius: 20px;
}

h1, h2, h3 {
    color: #0b3d91;
    font-weight: bold;
}

textarea {
    border-radius: 12px !important;
    font-family: Consolas, monospace;
    font-size: 15px;
    color: #000000;
    background-color: #f9f9f9 !important;
}

div.stButton > button {
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    font-size: 18px;
    border-radius: 12px;
    padding: 0.5rem 1.5rem;
    border: none;
    font-weight: bold;
    cursor: pointer;
}

.output-box {
    background-color: #1e1e1e;
    color: #00ff90;
    padding: 1rem;
    border-radius: 12px;
    font-family: Consolas, monospace;
    white-space: pre-wrap;
}

.error-box {
    background-color: #2b0000;
    color: #ff6b6b;
    padding: 1rem;
    border-radius: 12px;
    font-family: Consolas, monospace;
    white-space: pre-wrap;
}

.footer {
    text-align: center;
    color: #333333;
    margin-top: 2rem;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------
if "code" not in st.session_state:
    st.session_state.code = ""

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🎛 Controls")

if st.sidebar.button("🧹 Clear Code"):
    st.session_state.code = ""

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Templates")

if st.sidebar.button("Hello World"):
    st.session_state.code = "print('Hello World 🌍')"

if st.sidebar.button("Loop"):
    st.session_state.code = (
        "for i in range(5):\n"
        "    print('Count:', i)"
    )

if st.sidebar.button("Fibonacci"):
    st.session_state.code = (
        "n = 10\n"
        "a, b = 0, 1\n"
        "for _ in range(n):\n"
        "    print(a)\n"
        "    a, b = b, a + b"
    )

# --------------------------------------------------
# MAIN UI
# --------------------------------------------------
st.title("🐍 Python Terminal & Debugger")
st.write(
    "Type your Python code below and execute it like a real terminal. "
    "If errors occur, Gemini AI will help debug them."
)

code = st.text_area(
    "💻 Python Code Editor",
    height=300,
    value=st.session_state.code
)

st.session_state.code = code

run = st.button("▶ Execute Code")

# --------------------------------------------------
# CODE EXECUTION
# --------------------------------------------------
if run:
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    original_stdout = sys.stdout
    original_stderr = sys.stderr

    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer

    start_time = time.time()
    error_occurred = False

    try:
        exec(code, {})
    except Exception:
        error_occurred = True
        traceback.print_exc()
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    end_time = time.time()

    # OUTPUT
    st.subheader("📤 Execution Output")
    output_text = stdout_buffer.getvalue().strip() or "No output"
    st.markdown(
        f"<div class='output-box'>{output_text}</div>",
        unsafe_allow_html=True
    )

    # ERROR LOG
    error_text = stderr_buffer.getvalue().strip()
    if error_text:
        st.subheader("❌ Error Log")
        st.markdown(
            f"<div class='error-box'>{error_text}</div>",
            unsafe_allow_html=True
        )

    st.success(f"⏱ Execution Time: {end_time - start_time:.4f} seconds")

    # --------------------------------------------------
    # GEMINI DEBUGGING
    # --------------------------------------------------
    if error_occurred:
        with st.spinner("💡 Requesting assistance from Gemini AI…"):
            prompt = (
                "You are a Python debugging assistant.\n\n"
                f"Python Code:\n{code}\n\n"
                f"Error:\n{error_text}\n\n"
                "Explain the error and suggest a corrected version of the code."
            )
            try:
                gemini_response = call_gemini(prompt)
                st.subheader("🤖 Gemini AI Debugging Suggestion")
                st.markdown(
                    f"<div class='output-box'>{gemini_response}</div>",
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Gemini Error: {e}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    "<div class='footer'>⚠️ Educational & Debugging Tool Only</div>",
    unsafe_allow_html=True
)
