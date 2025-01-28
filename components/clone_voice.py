# components/clone_voice.py
import requests
import os

def generate_voice_clone():
    # Define the text to generate TTS
    texts = {
        "en": "The moon haunts you.",  # Example text in English
    }

    # Send a request to the /clone endpoint to generate TTS
    clone_response = requests.post(
        "http://localhost:8080/clone",
        json=texts
    )

    # If request fails, raise an exception
    if clone_response.content is None:
        raise Exception("Failed to generate TTS. No response received.")

    # Ensure the 'cloned' directory exists
    cloned_dir = "cloned"
    if not os.path.exists(cloned_dir):
        os.makedirs(cloned_dir)

    # Save and play the generated TTS audio
    output_file_path = os.path.join(cloned_dir, "output.wav")
    with open(output_file_path, "wb") as f:
        f.write(clone_response.content)

    # Check if the file was saved correctly
    if not os.path.exists(output_file_path):
        raise Exception(f"Error: The TTS audio file '{output_file_path}' was not created.")

    return output_file_path
