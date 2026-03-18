import streamlit as st
import groq

# Initialize Groq client
client = groq.Groq(api_key="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")
MODEL = "openai/gpt-oss-safeguard-20b"

def run_medic(code: str, mode: str) -> str:
    if not code.strip():
        return ""

    sys_prompt = (
        "You are a Senior Architect. Explain the logic errors first, then provide the optimized fix."
        if mode == "explain"
        else "Return ONLY the optimized, fixed code. No yapping. No markdown blocks."
    )

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": f"Fix/Optimize this:\n{code}"},
            ],
            temperature=0.1,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"❌ Maverick Offline: {e}")
        return ""

st.title("🚀 C0de Fixx\nMade By CyBoRgAiHaCkEr")
st.write("Paste your code below and choose a mode:")

code_input = st.text_area("Code to analyze", height=400)
mode = st.selectbox("Mode", ["fix", "explain"])

if st.button("Run"):
    with st.spinner("Maverick is analyzing..."):
        result = run_medic(code_input, mode)
    if result:
        st.success("Result ready!")
        st.code(result, language="python")
        st.button("Copy to clipboard", on_click=lambda: st.session_state.__setitem__("clipboard", result))
        if "clipboard" in st.session_state:
            st.text_area("Copied code", value=st.session_state.clipboard, height=200, read_only=True)
