FROM python:3.8.3-slim-stretch

ENV PYTHONWARNINGS=ignore
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
ENV DYNOMOCK_MOCKDIR=/var/lib/dynomock/data.json
ENV DYNOMOCK_TABLE_NAME=dockerdb

RUN touch default.json

RUN pip install dynomock --user

ENTRYPOINT [ "dynomock" ]