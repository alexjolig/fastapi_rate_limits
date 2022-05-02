FROM python:3.9.7-slim as base

WORKDIR /app

COPY requirements.txt .

COPY src/ /app

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
