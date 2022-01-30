FROM python:3.9.10-slim
WORKDIR /src
COPY . .
RUN pip install --requirement requirements.txt
CMD ["python", "src/producer.py"]
