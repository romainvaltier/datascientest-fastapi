FROM python:latest

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

EXPOSE 8000/TCP

CMD [ "uvicorn", "src.main:api", "--host", "0.0.0.0", "--port", "8000" ]