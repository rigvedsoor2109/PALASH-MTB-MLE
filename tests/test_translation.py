import sys

sys.path.append("/home/rigved/PALASH")

from ai.translator import translate_hindi_to_santali


hindi = "यह जोड़ का एक आसान सवाल है।"

santali = translate_hindi_to_santali(hindi)


print("\n==============================")
print("PALASH TRANSLATION RESULT")
print("==============================")
print("Hindi   :", hindi)
print("Santali :", santali)
print("==============================")
