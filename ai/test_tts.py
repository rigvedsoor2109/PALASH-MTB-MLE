from ai.tts import SantaliTTS


tts = SantaliTTS()

text = "ᱱᱚᱶᱟ ᱫᱚ ᱥᱟᱹᱨᱦᱟᱣ ᱠᱟᱹᱢᱤ ᱠᱟᱱᱟ."

output = "data/outputs/tts_test.wav"

tts.synthesize(text, output)

print()
print("DONE!")
print(f"Audio saved to: {output}")