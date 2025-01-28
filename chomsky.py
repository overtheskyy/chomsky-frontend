import streamlit as st
import requests
from components.record_voice import handle_voice_upload, cleanup_session, initialize_session
from components.send_voice import send_voice_to_server
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
        # Define the text to generate TTS
        texts = {
            "en": "Hello everyone, this is a test.",  # Example text in English
        }
        
        try:
            # Send a request to the /clone endpoint to generate TTS
            clone_response = requests.post(
                "http://localhost:8080/clone",
                json=texts
            )
            
            # Check if the response was successful
            if clone_response.status_code != 200:
                st.error(f"Error: Failed to generate TTS. Status code: {clone_response.status_code}")
                st.error(f"Details: {clone_response.text}")
                return

            # Save and play the generated TTS audio
            output_file_path = "output.wav"
            with open(output_file_path, "wb") as f:
                f.write(clone_response.content)
            
            # Check if the file was saved correctly
            if not os.path.exists(output_file_path):
                st.error(f"Error: The TTS audio file '{output_file_path}' was not created.")
                return

            st.success("TTS file generated successfully!")
            st.audio(output_file_path, format="audio/wav")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_session()