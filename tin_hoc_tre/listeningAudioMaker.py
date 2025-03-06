
import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# ELEVENLABS_API_KEY = os.getenv("sk_1fffec21a6dc1b1e7a991ec40aa96e30d2e6a593355dcf51")
client = ElevenLabs(
    api_key="sk_a57c251924a20d1a8e35dae5e5a73b5770b5008da29c54aa"
)


def text_to_speech_file(text, id):
    # Calling the text_to_speech conversion API with detailed parameters
   # voice = client.voices.get_all
    response = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    return response
