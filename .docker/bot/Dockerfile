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

COPY nextcloud_bot.py /app/
COPY nc_bot/ /app/nc_bot
EXPOSE 5000

CMD ["gunicorn", "-w", "4","-b", "0.0.0.0:5000", "nextcloud_bot:app"]
