"""Voice API router – Whisper STT + agent + Edge TTS."""

import io
import os
import tempfile
from pathlib import Path

import edge_tts
import whisper
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response

from src.backend.agent import ask_agent

router = APIRouter(prefix="/voice", tags=["voice"])

_model: whisper.Whisper | None = None

WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "base")
TTS_VOICE = os.environ.get("TTS_VOICE", "cs-CZ-VlastaNeural")


def get_model() -> whisper.Whisper:
    global _model
    if _model is None:
        _model = whisper.load_model(WHISPER_MODEL)
    return _model


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Přepíše nahraný audio soubor na text (Whisper)."""
    if not file.filename:
        raise HTTPException(400, "File is required")

    contents = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        model = get_model()
        if hasattr(model, "transcribe"):
            result = model.transcribe(tmp_path, language="cs")
            text = result.get("text", "")
        else:
            result = model.transcribe(str(tmp_path))
            text = result.get("text", "")

        return {"text": text.strip(), "language": "cs"}
    except Exception as e:
        raise HTTPException(500, f"Transcription failed: {e}")
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@router.post("/ask")
async def ask(question: str = Form(...), thread_id: str = Form("default")):
    """Pošle textový dotaz agentovi a vrátí textovou odpověď."""
    try:
        answer = await ask_agent(question, thread_id)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(500, f"Agent failed: {e}")


@router.post("/chat")
async def chat(
    file: UploadFile = File(...),
    thread_id: str = Form("default"),
):
    """Nahraje audio → přepíše → pošle agentovi → přečte odpověď → vrátí audio."""
    if not file.filename:
        raise HTTPException(400, "Audio file is required")

    # 1. Transcribe
    contents = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(contents)
        audio_path = tmp.name

    try:
        model = get_model()
        result = model.transcribe(audio_path, language="cs")
        question = result.get("text", "").strip()
        if not question:
            raise HTTPException(400, "No speech detected")
    except Exception as e:
        raise HTTPException(500, f"Transcription failed: {e}")
    finally:
        Path(audio_path).unlink(missing_ok=True)

    # 2. Agent
    try:
        answer = await ask_agent(question, thread_id)
    except Exception as e:
        raise HTTPException(500, f"Agent failed: {e}")

    # 3. TTS
    try:
        tts = edge_tts.Communicate(answer, TTS_VOICE)
        audio_data = b""
        async for chunk in tts.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
    except Exception as e:
        raise HTTPException(500, f"TTS failed: {e}")

    return Response(
        content=audio_data,
        media_type="audio/mpeg",
        headers={
            "X-Question": question,
            "X-Answer": answer,
        },
    )
