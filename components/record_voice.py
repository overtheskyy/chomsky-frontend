import streamlit as st
import os

def initialize_session():
    if 'recorded_audio_blob' not in st.session_state:
        st.session_state.recorded_audio_blob = None

    # Create recorded directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

def handle_voice_upload():
    initialize_session()
    voice_value = st.audio_input(label="Record voice", label_visibility="collapsed")
    
    if voice_value:
        audio_data = voice_value.getvalue()
        st.session_state.recorded_audio_blob = audio_data
        return st.session_state.recorded_audio_blob
    
    return None

def cleanup_session():
    # Clear session state
    for key in ['recorded_audio_blob']:
        if key in st.session_state:
            del st.session_state[key]