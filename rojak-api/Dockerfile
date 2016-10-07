FROM alpine

RUN apk --update add ncurses-libs && rm -rf /var/cache/apk/*

ARG VERSION
ENV PORT 4000
ENV APP_NAME rojak_api

# Enable runtime dynamic configuration via env vars
ENV REPLACE_OS_VARS true

EXPOSE $PORT

RUN mkdir /app
WORKDIR /app
COPY ./rel/$APP_NAME/releases/$VERSION/$APP_NAME.tar.gz /app/$APP_NAME.tar.gz
RUN tar -zxvf $APP_NAME.tar.gz && \
    rm $APP_NAME.tar.gz

CMD ["bin/rojak_api", "foreground"]
