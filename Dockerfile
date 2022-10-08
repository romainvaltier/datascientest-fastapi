FROM python:latest

WORKDIR /src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py ./

EXPOSE 8000/TCP

CMD [ "python", "-m", "uvicorn", "main:api", "--reload" ]