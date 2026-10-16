FROM python:3.12-alpine
WORKDIR /app
RUN apk upgrade --no-cache && adduser -D -u 10001 campusdesk
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER 10001
EXPOSE 8000
CMD ["sh","-c","python -m app.bootstrap && exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
