from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging
import base64

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


app = FastAPI()


class FileUpload(BaseModel):
    file_name: str
    file_content: str  # base64 encoded content

@app.post("/check_file")
async def upload_file(file: FileUpload):
    try:
        filename = file.file_name
        decoded_content = base64.b64decode(file.file_content)
        tmp_file_path = os.path.join(TMP_PATH, filename)
        with open(tmp_file_path, 'wb') as output_file:
            output_file.write(decoded_content)

        text_contents = process_file(tmp_file_path)
        os.remove(tmp_file_path)

        response = check_text(text_contents)
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class TextMessage(BaseModel):
    message: str

@app.post("/check_message")
async def receive_message(text: TextMessage):
    try:
        text_contents = text.message

        response = check_text(text_contents)
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level=logging.INFO)