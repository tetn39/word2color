# back
FROM python:3.12-slim

WORKDIR /app/backend

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]