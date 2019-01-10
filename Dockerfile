FROM  python
LABEL maintainer=achillesrasquinha@gmail.com

ENV PIPUPGRADEPATH=/usr/local/src/pipupgrade

RUN mkdir $PIPUPGRADEPATH

COPY . $PIPUPGRADEPATH

RUN pip install $PIPUPGRADEPATH

COPY ./docker/docker-entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["pipupgrade"]