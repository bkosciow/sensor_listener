FROM python:3.10
ARG PUID
ARG GUID

RUN useradd -u ${PUID} -m app

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/
COPY config.ini /app/
COPY .env /app/
COPY node_listener/ /app/node_listener
RUN pip install -r /app/requirements.txt

COPY flask_server.py /app/
COPY node_bot/ /app/node_bot
EXPOSE 5000

CMD ["gunicorn", "-w", "4","-b", "0.0.0.0:5000", "flask_server:app"]
