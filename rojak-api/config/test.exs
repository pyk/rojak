use Mix.Config

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :rojak_api, RojakAPI.Endpoint,
  http: [port: 4001],
  server: false

# Print only warnings and errors during test
config :logger, level: :warn

# Configure your database
config :rojak_api, RojakAPI.Repo,
  adapter: Ecto.Adapters.MySQL,
  username: System.get_env("DB_USERNAME") || "root",
  password: System.get_env("DB_PASSWORD") || "",
  database: System.get_env("DB_NAME") || "rojak_api_test",
  hostname: System.get_env("DB_HOST") || "localhost",
  pool: Ecto.Adapters.SQL.Sandbox
