use Mix.Config

# This secret file is no longer secret since we will use env
# variables. In this file we use the special strings ${ENV_NAME}
# to enable runtime configurations when running the compiled app.

config :rojak_api, RojakAPI.Endpoint,
  secret_key_base: "${SECRET_KEY_BASE}"

config :rojak_api, RojakAPI.Repo,
  adapter: Ecto.Adapters.MySQL,
  username: "${DB_USERNAME}",
  password: "${DB_PASSWORD}",
  database: "${DB_NAME}",
  hostname: "${DB_HOST}",
  pool_size: 20
