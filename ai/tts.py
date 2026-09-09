import torch
import soundfile as sf

from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer


MODEL_NAME = "ai4bharat/indic-parler-tts"

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"


class SantaliTTS:

    def __init__(self):

        print(f"Loading Santali TTS on {DEVICE}...")

        self.model = (
            ParlerTTSForConditionalGeneration
            .from_pretrained(MODEL_NAME)
            .to(DEVICE)
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        self.description_tokenizer = AutoTokenizer.from_pretrained(
            self.model.config.text_encoder._name_or_path
        )

        print("Santali TTS ready.")

    def synthesize(
        self,
        text: str,
        output_path: str = "santali_output.wav"
    ) -> str:

        description = (
            "Pushpa's voice delivers clear and friendly speech "
            "at a moderate speed and pitch. "
            "The recording has very clear audio."
        )

        description_inputs = self.description_tokenizer(
            description,
            return_tensors="pt"
        ).to(DEVICE)

        prompt_inputs = self.tokenizer(
            text,
            return_tensors="pt"
        ).to(DEVICE)

        audio = self.model.generate(
            input_ids=description_inputs.input_ids,
            attention_mask=description_inputs.attention_mask,
            prompt_input_ids=prompt_inputs.input_ids,
            prompt_attention_mask=prompt_inputs.attention_mask
        )

        audio = audio.cpu().numpy().squeeze()

        sf.write(
            output_path,
            audio,
            self.model.config.sampling_rate
        )

        print(f"Audio saved to: {output_path}")

        return output_path