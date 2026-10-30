FROM python:3.14-slim

RUN mkdir /app

WORKDIR /app

COPY app.py ./app.py
COPY requeriments.txt ./requeriments.txt

RUN pip install --upgrade pip
RUN pip install -r requeriments.txt

CMD ["fastapi", "run"]