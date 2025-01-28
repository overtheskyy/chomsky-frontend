import streamlit as st
from components.record_voice import handle_voice_upload, cleanup_session, initialize_session
from components.send_voice import send_voice_to_server

def main():
    st.title("Chomsky")
    
    initialize_session()
    
    st.text("Record your voice!")
    voice_path = handle_voice_upload()
    
    # Send audio to server when a button is clicked
    if voice_path and st.button("Send to Server"):
        response = send_voice_to_server(voice_path)

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_session()