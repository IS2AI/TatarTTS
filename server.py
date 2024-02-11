import io
import wave
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import FastAPI
from loguru import logger
from piper import PiperVoice
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from settings import settings

models = {}


class Model(str, Enum):
    male = 'male'
    female = 'female'

    def __str__(self):
        return self.value


@asynccontextmanager
async def lifespan(app):
    for model_name in map(str, Model):
        logger.debug("Loading model: {}", model_name)
        models[model_name] = PiperVoice.load(f'{settings.storage_folder}/{model_name}.onnx', use_cuda=False)
    yield
    models.clear()


app = FastAPI(title="TatarTTS", lifespan=lifespan)


class Config(BaseModel):
    text: str
    model: Model

    def run(self) -> io.BytesIO:
        """Text to Speech Recognition. Returns WAV audio file in the form of BytesIO object."""
        file = io.BytesIO()
        with wave.open(file, "wb") as wav_file:
            models[self.model.value].synthesize(self.text, wav_file)
        file.seek(0)
        return file


@app.post('/run')
async def run(config: Config):
    return StreamingResponse(config.run(), media_type="audio/wav")


def main():
    text = """И туган тел, и матур тел, әткәм-әнкәмнең теле! Дөньяда күп нәрсә белдем син туган тел аркылы. Габдулла Тукай"""
    piper_voice = PiperVoice.load('/storage/TatarTTS/female.onnx', use_cuda=True)
    with wave.open('qwe.wav', "wb") as wav_file:
        piper_voice.synthesize(text, wav_file)
    pass


if __name__ == '__main__':
    main()
