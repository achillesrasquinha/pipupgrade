<<<<<<< HEAD
=======


>>>>>>> template/master
FROM  python:3.7-alpine

LABEL maintainer=achillesrasquinha@gmail.com

ENV PIPUPGRADE_PATH=/usr/local/src/pipupgrade

RUN apk add --no-cache \
        bash \
        git \
    && mkdir -p $PIPUPGRADE_PATH

COPY . $PIPUPGRADE_PATH
COPY ./docker/entrypoint.sh /entrypoint.sh

<<<<<<< HEAD
RUN pip install $PIPUPGRADE_PATH

WORKDIR $PIPUPGRADE_PATH

=======
WORKDIR $PIPUPGRADE_PATH

RUN pip install -r ./requirements.txt && \
    python setup.py install

>>>>>>> template/master
ENTRYPOINT ["/entrypoint.sh"]

CMD ["pipupgrade"]