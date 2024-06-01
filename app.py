import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import numpy as np

st.title("Multi-user Audio Communication")

st.write("Enter the room and speak with mute/unmute functionality.")

# Custom audio processor
class AudioProcessor:
    def __init__(self):
        self.muted = False

    def recv(self, frame):
        # If muted, replace the audio data with silence
        if self.muted:
            audio_frame = frame.to_ndarray()
            audio_frame[:] = 0
            return av.AudioFrame.from_ndarray(audio_frame, format=frame.format)
        else:
            return frame

    def toggle_mute(self):
        self.muted = not self.muted

# RTC Configuration
rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# WebRTC Streamer
ctx = webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=rtc_configuration,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={
        "video": False,  # Disable video for this example
        "audio": True,
    },
)

# Mute/Unmute Button
if ctx.audio_processor:
    if st.button("Mute/Unmute"):
        ctx.audio_processor.toggle_mute()
        st.write("Muted" if ctx.audio_processor.muted else "Unmuted")
