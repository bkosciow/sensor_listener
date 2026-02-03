FROM python:3.14
ARG PUID
ARG GUID

RUN useradd -u ${PUID} -m app

RUN mkdir /app

WORKDIR /app

COPY requirements_mcp.txt /app/
COPY config.ini /app/
COPY .env /app/
COPY node_listener/ /app/node_listener
RUN pip install -r /app/requirements_mcp.txt

COPY mcp_server.py /app/
COPY mcp_server/ /app/mcp_server
EXPOSE 5000

CMD ["fastmcp", "run", "mcp_server.py:mcp", "--host", "0.0.0.0", "--transport", "http", "--port", "5000"]
