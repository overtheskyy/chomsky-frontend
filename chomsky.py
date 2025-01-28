import streamlit as st
from components.record_voice import handle_voice_upload, cleanup_session, initialize_session
from components.send_voice import send_voice_to_server
from components.clone_voice import generate_voice_clone
import os

def main():
    st.title("Chomsky")
    
    # Initialize the session
    initialize_session()
    
    # Step 1: Voice Upload Section
    st.subheader("Record Voice")
    voice_path = handle_voice_upload()
    
    # Step 2: Send to Server Button
    if st.button("Send to Server"):
        if voice_path:
            send_voice_to_server(voice_path)
            st.success("Voice file uploaded successfully!")
        else:
            st.warning("Please upload or record an audio file before sending!")
    
    # Step 3: Generate Voice Clone
    st.subheader("Generate Voice Clone")
    text_input = st.text_input("Enter the text for voice cloning:")
    language = st.selectbox("Select Language:", ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "hu", "ko", "ja", "hi"])  

    if st.button("Generate Voice Clone"):
        if text_input.strip():
            try:
                # Pass selected language and text
                output_file_path = generate_voice_clone(text_input, language)
                st.success("TTS file generated successfully!")
                st.audio(output_file_path, format="audio/wav")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter text for voice cloning.")

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_session()
