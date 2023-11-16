FROM python:3.10

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 

EXPOSE 8080

CMD ["python", "main.py"]