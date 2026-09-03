import torch
import soundfile as sf
from transformers import AutoModel


MODEL_NAME = "ai4bharat/indic-conformer-600m-multilingual"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading IndicConformer on {DEVICE}...")

model = AutoModel.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = model.to(DEVICE)
model.eval()

print("ASR model loaded!")


def transcribe(audio_path: str, language: str = "hi") -> str:

    audio, sample_rate = sf.read(audio_path)

    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    wav = torch.tensor(audio, dtype=torch.float32)

    wav = wav.unsqueeze(0)

    if sample_rate != 16000:
        import torchaudio

        resampler = torchaudio.transforms.Resample(
            orig_freq=sample_rate,
            new_freq=16000
        )

        wav = resampler(wav)

    wav = wav.to(DEVICE)

    with torch.no_grad():
        transcription = model(wav, language, "ctc")

    return transcription
