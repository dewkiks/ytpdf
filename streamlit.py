import streamlit as st
import asyncio
import younote  # Your updated younote.py
import config
from dotenv import load_dotenv
import os

load_dotenv()
st.title("YouTube Educational Notes Generator")

# --- Key Handling & Session State Initialization ---
if 'notes_generated' not in st.session_state:
    st.session_state.notes_generated = False
    st.session_state.markdown_content = ""
    st.session_state.pdf_bytes = None
    st.session_state.video_title = "YouTube_Notes"

api_key_input = st.text_input("Gemini API Key:", type="password")
api_key_to_use = api_key_input if api_key_input else os.getenv("GEMINI_API_KEY")
if api_key_to_use:
    config.set_api_key(api_key_to_use)

# --- UI Inputs ---
youtube_url = st.text_input("Enter YouTube URL:")
note_type = st.radio("Choose note type:", ["Short Notes", "Long Notes"])

# --- Generation Button Logic ---
if st.button("Generate Notes"):
    if not config.get_api_key():
        st.error("A Gemini API key is required.")
    elif not youtube_url:
        st.error("Please enter a YouTube URL.")
    else:
        with st.spinner("Analyzing video and generating notes..."):
            try:
                note_type_num = 1 if note_type == "Short Notes" else 2
                
                # MODIFIED: Run the workflow and capture the returned state dictionary
                final_state = asyncio.run(younote.extract_youtube_content(youtube_url, note_type_num))
                
                # Check for errors from the workflow
                if final_state.get("error"):
                    st.error(f"Workflow failed: {final_state['error']}")
                else:
                    # Populate session state from the returned dictionary
                    st.session_state.notes_generated = True
                    st.session_state.markdown_content = final_state.get("markdown_content")
                    st.session_state.pdf_bytes = final_state.get("pdf_bytes")
                    # You could extract a title here if you add it to the state
                    st.session_state.video_title = f"Notes_for_{youtube_url[-11:]}"

            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Display Results and Download Button ---
if st.session_state.notes_generated:
    st.success("✅ Notes generated successfully!")
    
    # Debug the PDF bytes
    if st.session_state.pdf_bytes:
        st.write(f"PDF size: {len(st.session_state.pdf_bytes)} bytes")
        st.write(f"PDF type: {type(st.session_state.pdf_bytes)}")
    else:
        st.error("PDF bytes are None!")
        st.write("Markdown content exists:", bool(st.session_state.markdown_content))
    
    with st.expander("View Markdown Notes"):
        st.markdown(st.session_state.markdown_content)
   
    # Only show download if PDF exists
    if st.session_state.pdf_bytes and len(st.session_state.pdf_bytes) > 0:
        st.download_button(
            label="⬇️ Download PDF",
            data=st.session_state.pdf_bytes,
            file_name=f"{st.session_state.video_title}.pdf",
            mime="application/pdf"
        )
    else:
        st.error("PDF generation failed - no download available")
        # Offer markdown download as fallback
        st.download_button(
            label="⬇️ Download as Markdown",
            data=st.session_state.markdown_content,
            file_name=f"{st.session_state.video_title}.md",
            mime="text/markdown"
        )
