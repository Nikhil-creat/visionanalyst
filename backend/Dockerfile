FROM python:3.11-slim AS build
WORKDIR /w
COPY requirements.txt .
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels
FROM python:3.11-slim
RUN useradd -r -u 1001 app
WORKDIR /app
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY . .
USER app
EXPOSE 8501
HEALTHCHECK CMD python -c "import urllib.request as u;u.urlopen('http://localhost:8501/_stcore/health')"
CMD ["streamlit","run","app.py","--server.address=0.0.0.0"]
