FROM msaraiva/elixir

RUN apk --update add erlang-crypto erlang-syntax-tools erlang-parsetools erlang-inets erlang-ssl erlang-public-key erlang-eunit \
    erlang-asn1 erlang-sasl erlang-erl-interface erlang-dev && \
    rm -rf /var/cache/apk/*

# Install hex and rebar
RUN mix local.hex --force && \
    mix local.rebar --force

# Install phoenix
RUN mix archive.install --force https://github.com/phoenixframework/archives/raw/master/phoenix_new.ez

WORKDIR /app
