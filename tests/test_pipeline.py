from ai.pipeline import process_audio


result = process_audio("/home/rigved/test.wav")

print("\n==============================")
print("       PALASH PIPELINE")
print("==============================")

print("Hindi:")
print(result["hindi"])

print("\nSantali:")
print(result["santali"])

print("\n==============================")
print("PIPELINE COMPLETE ✅")
print("==============================")

