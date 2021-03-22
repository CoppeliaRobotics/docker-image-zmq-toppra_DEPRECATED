FROM ubuntu:20.04
ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y python3-pip python3-zmq
RUN pip3 install --no-cache-dir cython numpy scipy matplotlib toppra
COPY toppra_server.py ./
EXPOSE 22505
CMD ["python3", "./toppra_server.py"]
