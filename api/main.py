from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
from ai.worksheet import generate_worksheet

import os
import shutil


from ai.translator import translate_hindi_to_santali
from ai.pipeline import process_audio


app = FastAPI(
    title="PALASH API",
    description="AI-powered vernacular pedagogy and translation backend",
    version="0.1.0",
    docs_url=None
)


os.makedirs("data/outputs", exist_ok=True)

app.mount(
    "/audio",
    StaticFiles(directory="data/outputs"),
    name="audio"
)


class TranslationRequest(BaseModel):
    text: str


@app.get("/docs", include_in_schema=False)
async def custom_swagger():
    swagger = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="PALASH API - Swagger UI"
    )

    html = swagger.body.decode()

    audio_player = """
    <div id="palash-audio-player"
         style="
            position: fixed;
            top: 15px;
            right: 25px;
            z-index: 9999;
            background: white;
            padding: 12px 16px;
            border-radius: 10px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.25);
         ">

        <strong>🔊 PALASH Santali Audio</strong>

        <br><br>

        <audio
            id="santali-player"
            controls
            preload="none"
            style="width: 280px;"
        >
            <source
                src="/audio/santali_output.wav"
                type="audio/wav"
            >
        </audio>

    </div>
    """

    html = html.replace(
        "</body>",
        audio_player + "</body>"
    )

    return HTMLResponse(content=html)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "PALASH",
        "service": "AI Backend",
    }


@app.post("/translate")
def translate(request: TranslationRequest):

    santali_text = translate_hindi_to_santali(
        request.text
    )

    return {
        "source_language": "Hindi",
        "target_language": "Santali",
        "input": request.text,
        "translation": santali_text,
    }


@app.post("/process-audio")
async def process_audio_endpoint(
    file: UploadFile = File(...)
):

    os.makedirs("data/uploads", exist_ok=True)

    file_path = os.path.join(
        "data/uploads",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = process_audio(file_path)

    return {
        "source_language": "Hindi",
        "target_language": "Santali",
        "filename": file.filename,
        "hindi": result["hindi"],
        "santali": result["santali"],
        "audio_url": "/audio/santali_output.wav",
        "play_url": "/play-audio"
    }


@app.get("/play-audio")
def play_audio():

    audio_path = "data/outputs/santali_output.wav"

    if not os.path.exists(audio_path):
        return {
            "error": "No Santali audio has been generated yet."
        }

    return FileResponse(
        audio_path,
        media_type="audio/wav",
        headers={
            "Content-Disposition": "inline"
        }
    )
class WorksheetRequest(BaseModel):
    class_name: str
    subject: str
    topic: str

@app.post("/generate-worksheet")
def create_worksheet(request: WorksheetRequest):

    worksheet = generate_worksheet(
        request.class_name,
        request.subject,
        request.topic
    )

    return worksheet