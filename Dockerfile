FROM  python:alpine
LABEL maintainer=achillesrasquinha@gmail.com

ENV PIPUPGRADEPATH=/usr/local/src/pipupgrade

RUN mkdir -p $PIPUPGRADEPATH

COPY . $PIPUPGRADEPATH

RUN pip install $PIPUPGRADEPATH

WORKDIR $PIPUPGRADEPATH

COPY ./docker/docker-entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["pipupgrade"]