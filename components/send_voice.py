import requests
import streamlit as st
import os

def send_voice_to_server(audio_data, base_dir="uploads"):
    try:
        # Validate if audio data is provided
        if not audio_data:
            st.warning("No audio data provided. Please record or upload a file before sending.")
            return None

        # Ensure the directory exists
        os.makedirs(base_dir, exist_ok=True)
        
        # Remove previous files in the directory
        for existing_file in os.listdir(base_dir):
            file_path = os.path.join(base_dir, existing_file)
            if os.path.isfile(file_path):
                try:
                    os.unlink(file_path)  # Remove file
                except Exception as e:
                    st.error(f"Error removing file {file_path}: {str(e)}")
        
        filename = os.path.join(base_dir, f"recording.wav")
        
        # Save the audio data
        with open(filename, "wb") as f:
            f.write(audio_data)

        # Send the file to the FastAPI server
        try:
            url = "http://localhost:8080/upload"  # Replace with your backend URL
            with open(filename, "rb") as file:
                files = {"file": file}
                response = requests.post(url, files=files)
                return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Server error: {str(e)}")
            return None
                
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return None
