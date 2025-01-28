import os
import requests

def generate_voice_clone(text: str, language: str) -> str:
    # Define payload for the cloning API
    payload = {
        language: text,  # Pass the selected language and text here
    }

    # API endpoint for voice cloning
    api_url = "http://localhost:8080/clone"
    response = requests.post(api_url, json=payload)

    # Ensure the 'cloned' directory exists
    cloned_dir = "cloned"
    os.makedirs(cloned_dir, exist_ok=True)

    # Save the generated audio file
    output_file_path = os.path.join(cloned_dir, "output.wav")
    with open(output_file_path, "wb") as audio_file:
        audio_file.write(response.content)

    # Verify file creation
    if not os.path.exists(output_file_path):
        raise Exception(f"The TTS audio file '{output_file_path}' was not created.")

    return output_file_path
