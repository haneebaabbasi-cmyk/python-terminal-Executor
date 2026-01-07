import streamlit as st
import io, sys, time, traceback
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
/* APP BACKGROUND - light and professional */
.stApp {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
}

/* MAIN CONTENT CARD */
.block-container {
    background-color: #ffffffee;
    padding: 2rem;
    border-radius: 20px;
}

/* HEADINGS */
h1, h2, h3 {
    color: #0b3d91;
    font-weight: bold;
}

/* PYTHON EDITOR */
textarea {
    border-radius: 12px !important;
    font-family: Consolas, monospace;
    font-size: 15px;
    color: #000000; /* black text */
    background-color: #f9f9f9 !important; /* light editor background */
}

/* RUN BUTTON */
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

/* OUTPUT BOX */
.output-box {
    background-color: #1e1e1e; /* dark terminal style */
    color: #00ff90;
    padding: 1rem;
    border-radius: 12px;
    font-family: Consolas, monospace;
}

/* ERROR BOX */
.error-box {
    background-color: #2b0000;
    color: #ff6b6b;
    padding: 1rem;
    border-radius: 12px;
    font-family: Consolas, monospace;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #333333;
    margin-top: 2rem;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🎛 Controls")

# Clear code button
if st.sidebar.button("🧹 Clear Code"):
    st.session_state.code = ""

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Templates")

if st.sidebar.button("Hello World"):
    st.session_state.code = "print('Hello World 🌍')"

if st.sidebar.button("Loop"):
    st.session_state.code = """for i in range(5):
    print("Count:", i)
"""

if st.sidebar.button("Fibonacci"):
    st.session_state.code = """n = 10
a, b = 0, 1
for _ in range(n):
    print(a)
    a, b = b, a + b
"""

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "code" not in st.session_state:
    st.session_state.code = ""

# --------------------------------------------------
# MAIN UI
# --------------------------------------------------
st.title("🐍 Python Terminal & Debugger")
st.write("Type your Python code below and execute it as if in a real terminal. If errors occur, Gemini AI will assist with debugging.")

# Python editor
code = st.text_area("💻 Python Code Editor", height=300, value=st.session_state.code)
st.session_state.code = code

# Run button
run = st.button("▶ Execute Code")

# --------------------------------------------------
# CODE EXECUTION
# --------------------------------------------------
if run:
    out = io.StringIO()
    err = io.StringIO()

    sys.stdout = out
    sys.stderr = err

    start = time.time()
    error_occurred = False

    try:
        exec(code)
    except Exception:
        error_occurred = True
        traceback.print_exc()
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    end = time.time()

    # Show output
    st.subheader("📤 Execution Output")
    st.markdown(f"<div class='output-box'>{out.getvalue() or 'No output'}</div>", unsafe_allow_html=True)

    # Show errors
    if err.getvalue():
        st.subheader("❌ Error Log")
        st.markdown(f"<div class='error-box'>{err.getvalue()}</div>", unsafe_allow_html=True)

    st.success(f"⏱ Execution Time: {end - start:.4f} seconds")

    # Gemini integration if error
    if error_occurred:
        with st.spinner("💡 Requesting assistance from Gemini AI…"):
            prompt = f"My Python code:\n{code}\nCaused this error:\n{err.getvalue()}\nPlease suggest a fix."
            try:
                gemini_response = call_gemini(prompt)
                st.subheader("🤖 Gemini AI Debugging Suggestion")
                st.markdown(f"<div class='output-box'>{gemini_response}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error calling Gemini: {e}")

# Footer
st.markdown("<div class='footer'>⚠️ Educational / Debugging Tool Only</div>", unsafe_allow_html=True)
