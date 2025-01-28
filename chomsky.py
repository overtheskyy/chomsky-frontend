# main.py
import streamlit as st
from components.record_voice import handle_voice_upload, cleanup_session, initialize_session
from components.send_voice import send_voice_to_server
from components.clone_voice import generate_voice_clone  # Import the new function
import os

def main():
    st.title("Chomsky")
    
    initialize_session()
    
    st.text("Record your voice!")
    voice_path = handle_voice_upload()
        
    # Always display the "Send to Server" button
    if st.button("Send to Server"):
        if voice_path:
            send_voice_to_server(voice_path)
            st.success("Voice file uploaded successfully!")
        else:
            st.warning("Please upload or record an audio file before sending!")
    
    # Always display the Generate Voice Clone button
    if st.button("Generate Voice Clone"):
        try:
            output_file_path = generate_voice_clone()
            st.success("TTS file generated successfully!")
            st.audio(output_file_path, format="audio/wav")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_session()
