# Personal Data Checker Microservice

## Overview

This microservice is designed to check if any personal data has been shared in a message or file. It uses FastAPI for handling HTTP requests and responses. The service provides two main endpoints:

1. `/check_file`: Accepts a file (in base64 format) and checks its contents for personal data. Supported file types: pdf, docx, xlsx, txt.
2. `/check_message`: Accepts a text message and checks it for personal data.

## Endpoints

### 1. `/check_file`

- **Method:** `POST`
- **Description:** This endpoint checks the contents of an uploaded file for personal data.
- **Request Body:**
  - `username` (string): The username of the user.
  - `filename` (string): The name of the file. Used to check if any data is shared in the name.
  - `doc_type` (string): The type of the file. Supported file types: pdf, docx, xlsx, txt.
  - `data` (string): The content of the file, encoded in base64.
- **Response:**
  - `status` (string): The status of the request. "ok" if nothing was found. Other statuses: "sensitive_information", "swear_words", "offensive_communication".
  - `explanation` (string): Explanation of what was found, if applicable.
- **Example Request:**
  ```json
  {
    "username": "klopotuk",
    "filename": "Dyploma Alex Shevtsov",
    "doc_type": "docx",
    "data": "base64"
  }
  ```
- **Example Response:**
  ```json
  {
    "status": "sensitive_information",
    "explanation": "The text contains the full name 'Alex Shevtsov', which is considered personal data."
  }
  ```

### 2. `/check_message`

- **Method:** `POST`
- **Description:** This endpoint checks a text message for personal data.
- **Request Body:**
  - `username` (string): The username of the user.
  - `message` (string): The text message to be checked.
- **Response:**
  - `status` (string): The status of the request. "ok" if nothing was found. Other statuses: "sensitive_information", "swear_words", "offensive_communication".
  - `explanation` (string): Explanation of what was found, if applicable.
- **Example Request:**
  ```json
  {   
    "username": "klopotuk",
    "message":"Подскажите, пожалуйста, какой именно блять отчёт вы хотите сделать по истории средневековой бетбумии."
  }
  ```
- **Example Response:**
  ```json
  {
    "status": "swear_words",
    "explanation": "The text contains the swear word 'блять'."
  }
  ```

## Running the Application
Before the start add a .env file with an environment variable `OPENAI_API_KEY`.
After that start the application, using the following command:
`docker-compose up --build`

The application is hosted on `8001` port.


## Directory Structure

- `main.py`: The main application file containing the FastAPI app and endpoints.
- `file_check.py`: Contains the logic for processing files.
- `llm.py`: Contains the logic for checking text for personal data.
- `temp/`: Temporary directory for storing uploaded files during processing.