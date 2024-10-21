import json

import openai
import whisper
import requests
import torch
from loguru import logger

from src.constants import INTERVIEW_POSTION, API_SERVICE_KEY, OUTPUT_FILE_NAME, DEVICE, URL

openai.api_key = API_SERVICE_KEY

torch.cuda.init()

SYSTEM_PROMPT = f"""You are interviewing for a {INTERVIEW_POSTION} position.
You will receive an text of the question. It may not be complete. You need to understand the question and write 
an answer to it.\n
"""
SHORTER_INSTRACT = "Concisely respond, limiting your answer to 70 words. Answer in Russian."
LONGER_INSTRACT = """Before answering, take a deep breath and think one step at a time. 
Believe the answer in no more than 150 words. Answer in Russian."""

model = whisper.load_model("medium")


def transcribe_audio(path_to_file: str = OUTPUT_FILE_NAME) -> str:
    with open(path_to_file, "rb"):
        try:
            options = {
                "language": "russian",
                "task": "transcribe"
            }
            with torch.cuda.device(DEVICE):
                transcript = model.transcribe(path_to_file, **options)
        except Exception as error:
            logger.error(f"Can't transcribe audio: {error}")
            raise error
    return transcript["text"]


def generate_answer(transcript: str, short_answer: bool = True, temperature: float = 0.2) -> str:
    if short_answer:
        system_prompt = SYSTEM_PROMPT + SHORTER_INSTRACT
    else:
        system_prompt = SYSTEM_PROMPT + LONGER_INSTRACT
    try:
        payload = {
            "model": "llama-3",
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": transcript}, ]
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": 'c8eb8ae7-3f97-4255-81b9-bb0e1e1a8663'
        }
        response = requests.post(URL, json=payload, headers=headers)

    except Exception as error:
        logger.error(f"Can't generate answer: {error}")
        raise error
    data = response.text
    lines = [line.replace('data: ', '').strip() for line in data.splitlines() if line.strip()]

    full_text = ""

    for line in lines:
        if line == "[DONE]":
            continue
        try:
            json_object = json.loads(line)

            content = json_object['choices'][0]['delta'].get('content', '')
            full_text += content
        except json.JSONDecodeError as e:
            break

    return full_text
