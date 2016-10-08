use Mix.Config

config :rojak_api, RojakAPI.Endpoint,
  http: [port: {:system, "PORT"}],
  url: [host: "localhost", port: {:system, "PORT"}],
  version: Mix.Project.config[:version]

# Do not print debug messages in production
config :logger, level: :info

# ## Using releases
#
# If you are doing OTP releases, you need to instruct Phoenix
# to start the server for all endpoints:
config :phoenix, :serve_endpoints, true

# Finally import the config/prod.secret.exs
# which should be versioned separately.
import_config "prod.secret.exs"
