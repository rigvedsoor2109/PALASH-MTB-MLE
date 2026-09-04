from ai.asr import transcribe
from ai.translator import translate_hindi_to_santali


def process_audio(audio_path: str) -> dict:
    print("\n🎤 Processing teacher audio...")

    hindi_text = transcribe(audio_path, "hi")

    print("\nHindi:")
    print(hindi_text)

    print("\n🌐 Translating to Santali...")

    santali_text = translate_hindi_to_santali(hindi_text)

    print("\nSantali:")
    print(santali_text)

    return {
        "hindi": hindi_text,
        "santali": santali_text
    }
