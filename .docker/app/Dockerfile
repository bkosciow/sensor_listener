FROM python:3.14
ARG PUID
ARG GUID

RUN apt update && apt upgrade -y && apt install -y --no-install-recommends supervisor sudo cron
RUN mkdir -p \
    /var/log/supervisord \
    /var/run/supervisord \
;

RUN useradd -u ${PUID} -m app

COPY .docker/app/supervisord.conf /
COPY .docker/app/crontab /
RUN crontab -u app /crontab

RUN mkdir /app
RUN mkdir /supervisordlog
RUN mkdir /cronlog && chmod -R 0777 /cronlog

WORKDIR /app

COPY requirements.txt /app/
COPY config.ini /app/
COPY .env /app/
COPY node_listener/ /app/node_listener
RUN pip install -r /app/requirements.txt

COPY server.py /app/
COPY openaq_worker.py /app/

CMD ["/usr/bin/supervisord", "-c", "/supervisord.conf"]

