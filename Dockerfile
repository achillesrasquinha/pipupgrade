FROM  python:alpine
LABEL maintainer=achillesrasquinha@gmail.com

ENV PIPUPGRADEPATH=/usr/local/src/pipupgrade

RUN apk add --no-cache bash git

RUN mkdir -p $PIPUPGRADEPATH

COPY . $PIPUPGRADEPATH

RUN pip install $PIPUPGRADEPATH

WORKDIR $PIPUPGRADEPATH

ENTRYPOINT ["/usr/local/src/pipupgrade/docker/entrypoint.sh"]

CMD ["pipupgrade"]