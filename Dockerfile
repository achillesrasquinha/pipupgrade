

FROM  python:3.7-alpine

LABEL maintainer=achillesrasquinha@gmail.com

ENV PIPUPGRADE_PATH=/usr/local/src/pipupgrade

RUN apk add --no-cache \
        bash \
        git \
    && mkdir -p $PIPUPGRADE_PATH

COPY . $PIPUPGRADE_PATH
COPY ./docker/entrypoint.sh /entrypoint.sh

RUN pip install $PIPUPGRADE_PATH

WORKDIR $PIPUPGRADE_PATH

ENTRYPOINT ["/entrypoint.sh"]

CMD ["pipupgrade"]