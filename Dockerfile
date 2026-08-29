FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
RUN pip install --upgrade pip && pip install .[test]
COPY . /app
CMD ["python", "-m", "services.api_gateway.main"]
