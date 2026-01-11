FROM python:3.14
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

COPY server.py /app/


CMD ["python", "server.py"]
