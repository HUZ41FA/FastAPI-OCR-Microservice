import pathlib
from fastapi import FastAPI, Body, Request, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse 
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings
from functools import lru_cache
import io
import uuid
from .ocr import img_to_text

class Settings(BaseSettings):
    debug : bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings() 


DEBUG = get_settings().debug

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR/ "upload"
templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))
app = FastAPI(
    title="OCR Microservice"
)

@app.get("/", response_class=HTMLResponse)
def hello(request : Request, settings : Settings = Depends(get_settings)):
    print(request)
    return templates.TemplateResponse("home.html", {"request":request})


@app.post("/img-echo")
async def hello_post(file : UploadFile = File(...)):
    file_bytes = io.BytesIO(await file.read())
    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    destination = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"

    with open(str(destination), 'wb') as out:
        out.write(file_bytes.read())
    return img_to_text(destination)
