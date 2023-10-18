FROM python:3.10-slim

WORKDIR /app

# Define build-time argument
ARG OPENAI_API_KEY=123

# Set it as an environment variable (optional)
ENV OPENAI_API_KEY=$API_KEY


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


COPY ./src /app

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]




