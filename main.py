from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
import shutil
import subprocess

app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Music Video AI Backend Running"}

@app.post("/generate")
async def generate_video(
    audio: UploadFile = File(...),
    lyrics: str = Form(...)
):
    job_id = str(uuid.uuid4())

    audio_path = os.path.join(UPLOAD_FOLDER, f"{job_id}.mp3")
    output_path = os.path.join(OUTPUT_FOLDER, f"{job_id}.mp4")

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # Simple placeholder video (black screen + audio)
    subprocess.run([
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=c=black:s=1280x720:d=10",
        "-i", audio_path,
        "-shortest",
        "-c:v", "libx264",
        "-c:a", "aac",
        output_path
    ])

    return JSONResponse({
        "status": "complete",
        "video_file": f"/video/{job_id}"
    })

@app.get("/video/{job_id}")
def get_video(job_id: str):
    return {"message": f"Video ready for job {job_id}"}
