FROM python:3.14
ARG PUID
ARG GUID

RUN useradd -u ${PUID} -m app

RUN mkdir /app

WORKDIR /app

COPY requirements_bot.txt /app/
COPY config.ini /app/
COPY .env /app/
COPY node_listener/ /app/node_listener
RUN pip install -r /app/requirements_bot.txt

COPY nextcloud_bot.py /app/
COPY nc_bot/ /app/nc_bot
EXPOSE 5000

CMD ["uvicorn", "--workers", "4","--host", "0.0.0.0", "--port", "5000", "nextcloud_bot:app"]
