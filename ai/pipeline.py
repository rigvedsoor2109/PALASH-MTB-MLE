from ai.asr import transcribe
from ai.translator import translate_hindi_to_santali
from ai.tts import SantaliTTS

import os


tts = SantaliTTS()


def process_audio(audio_path: str) -> dict:
    print("\n🎤 Processing teacher audio...")

    hindi_text = transcribe(audio_path, "hi")

    print("\nHindi:")
    print(hindi_text)


    print("\n🌐 Translating to Santali...")

    santali_text = translate_hindi_to_santali(hindi_text)

    print("\nSantali:")
    print(santali_text)


    print("\n🔊 Generating Santali speech...")

    os.makedirs("data/outputs", exist_ok=True)

    output_path = "data/outputs/santali_output.wav"

    tts.synthesize(
        santali_text,
        output_path
    )

    print("\n✅ Santali audio generated:")
    print(output_path)

    return {
        "hindi": hindi_text,
        "santali": santali_text,
        "audio_path": output_path
    }