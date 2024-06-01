import streamlit as st
import speech_recognition as sr

def recognize_speech(recognizer):
    """Continuously listens for speech and returns the transcript."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Improve clarity
        audio_stream = recognizer.listen(source)

    try:
        transcript = recognizer.recognize_google(audio_stream)  # Adjust for chosen service
        return transcript
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results from speech recognition service: {e}")
        return ""

# Initialize variables and layout
st.title("Real-time Speech-to-Text")
user_name = st.text_input("Enter your name")

if user_name:
    st.write("Enable continuous speech recognition (check box to start).")
    is_listening = st.checkbox("Start Transcribing", key="is_listening")  # Add key

    # Create a recognizer instance
    recognizer = sr.Recognizer()

    if is_listening:
        transcript = ""
        st.write("Speak now!")
        # text = ""

        # Continuously listen for speech in a loop
        while True:
            transcript = recognize_speech(recognizer)
            # text = text+transcript
            if transcript.strip():
                st.write(f"**{user_name}:** {transcript}")

else:
    st.write("Please enter your name.")
