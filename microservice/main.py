from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging
import base64
import tempfile
import time
import json

from file_check import process_file
from llm import check_text

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("httpcore").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger("personal-data-checker")

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
TMP_PATH = os.path.join(BASE_PATH, 'temp')
if not os.path.exists(TMP_PATH):
    os.mkdir(TMP_PATH)

BIG_MODEL_NAME = "gpt-5-mini-2025-08-07"
LIGHT_MODEL_NAME = "gpt-5-nano-2025-08-07"

LARGE_FILE_LENGTH_LIMIT = 4000

app = FastAPI()


class FileUpload(BaseModel):
    username: str
    filename: str
    doc_type: str
    data: str  # base64 encoded content

file_extensions = {
        'DOCX': '.docx',
        'PDF': '.pdf',
        'XLSX': '.xlsx',
        'TXT': '.txt'
    }

@app.post("/check_file")
async def upload_file(file: FileUpload):
    try:

        file_extension = file_extensions[file.doc_type.upper()]
        decoded_data = base64.b64decode(file.data)
        
        with tempfile.NamedTemporaryFile(dir=TMP_PATH, suffix=file_extension, delete=False) as temp_file:
            temp_file.write(decoded_data)
            temp_file_name = temp_file.name
            logger.info(f'Temporary file created: {temp_file_name}')
        
        text_contents = f"File name: {file.filename}\n" + process_file(temp_file_name)
        os.remove(temp_file_name)

        if len(text_contents) < LARGE_FILE_LENGTH_LIMIT:
            model_mame = BIG_MODEL_NAME
        else:
            model_mame = LIGHT_MODEL_NAME
        response = check_text(text_contents, model_mame)
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class TextMessage(BaseModel):
    username: str
    message: str

@app.post("/check_message")
async def receive_message(text: TextMessage):
    try:
        text_contents = text.message

        response = check_text(text_contents, BIG_MODEL_NAME)
        return json.loads(response)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level=logging.ERROR)