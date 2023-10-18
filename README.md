# Streamlit GenAI showcase

## Description 
You upload a file , then you ask questions in natural language. These are fed to a LLM which responds your questions with context.

## Usage
You need a .env file with your credentials and you pass it to your container during runtime
```bash
docker build -t streamlit .
docker run --env-file .env -p 8501:8501 streamlit
```