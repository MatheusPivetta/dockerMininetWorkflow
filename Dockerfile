FROM iwaseyusuke/mininet:latest
WORKDIR /code
ENV TOPOLOGY_FILE=topology.py
RUN mn TOPOLOGY_FILE