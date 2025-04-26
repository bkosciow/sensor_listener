FROM python:3.10
RUN apt update && apt upgrade -y
RUN mkdir /node_listener
WORKDIR /node_listener
COPY . /node_listener/
RUN pip install -r requirements.txt

CMD ["python", "./server.py"]
