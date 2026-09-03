import sys

sys.path.append("/home/rigved/PALASH")

from ai.asr import transcribe


audio_file = "/home/rigved/test.wav"

text = transcribe(audio_file)

print("\n==============================")
print("PALASH ASR RESULT")
print("==============================")
print("Hindi:", text)
print("==============================")

