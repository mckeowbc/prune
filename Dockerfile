FROM python:3-slim

ADD prune.py /usr/bin/prune.py

ENTRYPOINT [ "/usr/bin/prune.py" ]