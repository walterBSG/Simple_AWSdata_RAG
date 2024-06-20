
# Property Valuation Model

This repository contains a comprehensive solution for estimating property valuations for a real estate client in Chile. The project includes a robust pipeline, an API, and Jupyter notebooks for database configuration and testing. The solution is designed to be deployable using Docker and follows best coding practices.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [To-Do](#to-do)

## Project Structure

```
├── .env
├── app.py
├── requirements.txt
├── api
│   ├── controller.py
│   ├── routes.py
│   └── __pycache__
│       ├── controller.cpython-311.pyc
│       └── routes.cpython-311.pyc
├── db
│   ├── database.py
│   ├── manage_db.py
│   └── __pycache__
│       ├── database.cpython-311.pyc
│       └── manage_db.cpython-311.pyc
├── notebooks
│   ├── config_db.ipynb
│   ├── test_API.ipynb
│   └── upload_database.ipynb
└── utils
    ├── chunker.py
    ├── openai_utils.py
    └── __pycache__
        ├── chunker.cpython-311.pyc
        └── openai_utils.cpython-311.pyc
```

## Installation

### Prerequisites
- Python 3.11
- Other requirements listed in `requirements.txt`

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/walterBSG/loka_test.git
    cd property-valuation-model
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    - Copy the `.env.example` to `.env` and fill in the necessary environment variables.

## Usage

### Running the Application
To run the application locally, use the following command:
```bash
uvicorn app:app
```

### Running the Notebooks
The `notebooks` directory contains Jupyter notebooks for configuring the database, testing the API, and uploading the database. To run these notebooks, use Jupyter Lab or Jupyter Notebook.

### Setting up the Database
- Configure the database:
    - Open `config_db.ipynb` and run the code.
- Upload data to the database:
    - Open `upload_database.ipynb` and run the code.

## API Documentation

### POST /chat
Handles chat queries in the OpenAI format.

- **Request Body**:
  - `query` (string): The query to be handled by the chat function.

### POST /query
Send a single message to the API to test with a simpler input (no chat).

- **Request Body**:
  - `query` (string): The query to be handled by the query function.

### POST /upsert
Uploads and processes a file.

- **Request Body**:
  - `file` (UploadFile): The file to be uploaded and processed.

### DELETE /delete
Deletes a specified file.

- **Request Body**:
  - `file_name` (string): The name of the file to be deleted.

### POST /index
Indexes data.

- **No request body required**.

### GET /
Root endpoint. Provides a welcome message and information on available endpoints.

## To-Do

- Implement hybrid search for better data retrieval.
- Develop a client for proper use of chat.
- Improve handling of file uploads. (handle more types of files)
- Use semantic chunking for better database chunks.
- Dockerize the solution.
