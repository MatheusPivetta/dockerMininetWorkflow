FROM iwaseyusuke/mininet:latest
VOLUME /APP/workflow-volume
WORKDIR /APP/workflow-volume
COPY workflow-volume/entrypoint.sh /APP/workflow-volume
COPY workflow-volume/topology.py /APP/workflow-volume
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh"]
