# app.py

import streamlit as st
from urllib.parse import urlparse, parse_qs

from transcript_loader import get_transcript_with_language_selection
from retriever_utils import get_retriever_from_transcript
from model_selector import get_llm
from query_engine import build_qa_chain

st.set_page_config(page_title="🎥 YouTube RAG Assistant", layout="centered")
st.title("🎥 YouTube RAG Assistant")

# Session memory
if "transcript_text" not in st.session_state:
    st.session_state.transcript_text = None

# Model selection
st.markdown("### 🔧 Select your preferred AI model")

model_choice = st.selectbox(
    "Choose a model:",
    ["OpenAI (GPT)", "Gemini (Google)", "Ollama (Local)"]
)

api_key = None
if model_choice in ["OpenAI (GPT)", "Gemini (Google)"]:
    api_key = st.text_input("🔑 Enter your API Key", type="password")

# YouTube URL input
youtube_url = st.text_input("Enter YouTube Video URL:")

def extract_video_id(url):
    try:
        parsed = urlparse(url)
        if parsed.hostname == "youtu.be":
            return parsed.path[1:]
        if "youtube.com" in parsed.hostname:
            return parse_qs(parsed.query)["v"][0]
    except:
        return None

if youtube_url:
    video_id = extract_video_id(youtube_url)

    if not video_id:
        st.error("Invalid YouTube URL.")
    else:
        st.info("🔍 Checking for transcript...")
        transcript_data, lang_or_options = get_transcript_with_language_selection(video_id)

        if transcript_data:
            transcript_text = transcript_data
            st.session_state.transcript_text = transcript_text
            st.success(f"✅ Transcript loaded in: {lang_or_options}")
            with st.expander("📄 Transcript Preview"):
                st.write(transcript_text)

        elif lang_or_options:
            chosen_lang = st.selectbox("Choose transcript language:", options=lang_or_options)
            if st.button("Load Selected Transcript"):
                selected_transcript_data, selected_lang = get_transcript_with_language_selection(video_id, chosen_lang)
                if selected_transcript_data:
                    transcript_text = " ".join([t.text for t in selected_transcript_data])
                    st.session_state.transcript_text = transcript_text
                    st.success(f"✅ Loaded transcript in: {selected_lang}")
                    with st.expander("📄 Transcript Preview"):
                        st.write(transcript_text)
                else:
                    st.error("Failed to load that language.")
        else:
            st.error("🚫 No transcripts found.")

# If transcript is loaded, allow questions
if st.session_state.transcript_text:
    transcript_text = st.session_state.transcript_text
    st.markdown("---")
    st.subheader("💬 Ask or Summarize")

    user_question = st.text_input("Type your question:")
    summarize = st.button("📝 Summarize Video")

    retriever, _ = get_retriever_from_transcript(transcript_text, model_choice, api_key)
    llm = get_llm(model_choice, api_key)
    chain = build_qa_chain(retriever, llm, api_key if model_choice == "Gemini (Google)" else None)

    if user_question:
        with st.spinner("💡 Thinking..."):
            answer = chain(user_question)
        st.markdown("### 💬 Answer")
        st.write(answer)

    if summarize:
        with st.spinner("🧠 Summarizing..."):
            summary = chain("Summarize the entire video.")
        st.markdown("### 📝 Summary")
        st.write(summary)

