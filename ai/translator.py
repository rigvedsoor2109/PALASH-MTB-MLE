import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor


MODEL_NAME = "ai4bharat/indictrans2-indic-indic-dist-320M"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

SRC_LANG = "hin_Deva"
TGT_LANG = "sat_Olck"


print(f"Loading IndicTrans2 on {DEVICE}...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
)

model = model.to(DEVICE)
model.eval()

processor = IndicProcessor(inference=True)

print("Translation model loaded!")


def translate_hindi_to_santali(text: str) -> str:

    batch = processor.preprocess_batch(
        [text],
        src_lang=SRC_LANG,
        tgt_lang=TGT_LANG
    )

    inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt"
    )

    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        generated_tokens = model.generate(
            **inputs,
            use_cache=True,
            min_length=0,
            max_length=256,
            num_beams=5,
            num_return_sequences=1
        )

    decoded = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )

    translations = processor.postprocess_batch(
        decoded,
        lang=TGT_LANG
    )

    return translations[0]
