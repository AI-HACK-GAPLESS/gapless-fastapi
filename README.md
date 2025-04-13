# Gapless-fastapi

gapless-fastapi is a FastAPI-based backend service designed to provide intelligent explanations of technical terms and concepts. It integrates with OpenAI’s GPT models to generate concise summaries and keyword explanations, enhancing user understanding of complex texts.


## Features
- Explain API: Processes input text to extract keywords and generate summaries.
- Explain-More API: Provides additional explanations based on previous results.
- Dictionary Upload: Allows users to upload custom dictionaries in PDF or text format for personalized term explanations.
- Keyword Management: Stores and manages extracted keywords for future reference.
- Server-Specific Dictionaries: Supports server-specific dictionaries to tailor explanations based on the server context.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/AI-HACK-GAPLESS/gapless-fastapi.git
cd gapless-fastapi
```
2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
4.	Configure environment variables:
Create a .env file in the root directory and add the following:
```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_database_connection_string
```
## Usage
1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```
2. Access the API documentation:
Navigate to http://localhost:8000/docs to explore and test the available endpoints.

## API Endpoints(core)
- POST /explain: Accepts text input and returns extracted keywords and a summary.
- POST /explain-more: Provides additional explanations based on previous results.
- POST /upload-dict/pdf: Uploads a PDF file containing custom dictionary terms.
- POST /upload-dict/text: Uploads text input containing custom dictionary terms.



   
