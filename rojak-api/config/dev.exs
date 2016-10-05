use Mix.Config

# For development, we disable any cache and enable
# debugging and code reloading.
#
# The watchers configuration can be used to run external
# watchers to your application. For example, we use it
# with brunch.io to recompile .js and .css sources.
config :rojak_api, RojakAPI.Endpoint,
  http: [port: 4000],
  debug_errors: true,
  code_reloader: true,
  check_origin: false,
  watchers: []


# Do not include metadata nor timestamps in development logs
config :logger, :console, format: "[$level] $message\n"

# Set a higher stacktrace during development. Avoid configuring such
# in production as building large stacktraces may be expensive.
config :phoenix, :stacktrace_depth, 20

# Configure your database
config :rojak_api, RojakAPI.Repo,
  adapter: Ecto.Adapters.MySQL,
  username: System.get_env("DB_USERNAME") || "root",
  password: System.get_env("DB_PASSWORD") || "",
  database: System.get_env("DB_NAME") || "rojak_api_dev",
  hostname: System.get_env("DB_HOST") || "localhost",
  pool_size: 10
