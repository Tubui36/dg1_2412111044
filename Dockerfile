FROM python:3.12-slim
WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m -u 1000 appuser

COPY app/ .
RUN chown -R appuser:appuser /app
USER appuser

ENV PORT=5000
EXPOSE 5000
CMD ["python", "app.py"]