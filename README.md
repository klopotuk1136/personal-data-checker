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
  - `file_name` (string): The name of the file. Supported file types: pdf, docx, xlsx, txt.
  - `file_content` (string): The content of the file, encoded in base64.
- **Response:**
  - `is_personal_data_found` (boolean): Indicates if personal data was found.
  - `category` (string): The category of the personal data found (e.g., "surname").
  - `explanation_if_found` (string): Explanation of what was found, if applicable.
- **Example Request:**
  ```json
  {
    "file_name": "example.pdf",
    "file_content": "JVBERi0xLjcKCjEgMCBv..."
  }
  ```
- **Example Response:**
  ```json
  {
    "is_personal_data_found": true,
    "category": "surname",
    "explanation_if_found": "The text includes the name 'John Doe', which contains a first name and a surname."
  }
  ```

### 2. `/check_message`

- **Method:** `POST`
- **Description:** This endpoint checks a text message for personal data.
- **Request Body:**
  - `message` (string): The text message to be checked.
- **Response:**
  - `is_personal_data_found` (boolean): Indicates if personal data was found.
  - `category` (string): The category of the personal data found (e.g., "surname").
  - `explanation_if_found` (string): Explanation of what was found, if applicable.
- **Example Request:**
  ```json
  {
    "message": "My name is John Doe."
  }
  ```
- **Example Response:**
  ```json
  {
    "is_personal_data_found": true,
    "category": "surname",
    "explanation_if_found": "The text includes the name 'John Doe', which contains a first name and a surname."
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