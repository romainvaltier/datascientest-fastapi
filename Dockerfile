FROM python:latest

WORKDIR /test

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py ./

EXPOSE 8000

CMD [ "uvicorn", "main:api", "--reload" ]