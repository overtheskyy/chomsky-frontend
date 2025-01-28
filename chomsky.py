import streamlit as st
from components.record_voice import handle_voice_upload, cleanup_session, initialize_session
from components.send_voice import send_voice_to_server
from components.clone_voice import generate_voice_clone
import os


def main():
    st.title("Chomsky")
    
    # Initialize the session
    initialize_session()

    # Input for user message
    user_message = st.text_input("Enter your question:")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Initialize chat history

    if st.button("Send"):
        if user_message.strip():
            from groq import Groq

            api_key = st.secrets["groq"]["api_key"]

            try:
                # Initialize Groq client
                client = Groq(api_key=api_key)

                # Prepare the messages for the chat completion
                messages = [{"role": "system", "content": "You are a language-learning chatbot named Chomsky."}]

                # Add previous chat history to messages
                for chat in st.session_state.chat_history:
                    messages.append({"role": "user", "content": chat["user"]})
                    messages.append({"role": "assistant", "content": chat["bot"]})

                # Add the current user message
                messages.append({"role": "user", "content": user_message})

                # Get the completion response
                completion = client.chat.completions.create(
                    model="deepseek-r1-distill-llama-70b",
                    messages=messages,
                    temperature=1,
                    max_completion_tokens=500,
                    top_p=1,
                    stream=False,
                    stop=None,
                )

                # Correctly access the chatbot's response using dot notation
                bot_response = completion.choices[0].message.content

                # Save the current user message and bot response to chat history
                st.session_state.chat_history = [{"user": user_message, "bot": bot_response}]  # Keep only the latest chat

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a message.")

    # Display only the current chat
    if st.session_state.chat_history:
        latest_chat = st.session_state.chat_history[0]
        st.write(f"**You:** {latest_chat['user']}")
        st.write(f"**Chomsky:** {latest_chat['bot']}")

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
