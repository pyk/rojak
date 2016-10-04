defmodule RojakAPI.Router do
  use RojakAPI.Web, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/api", RojakAPI do
    pipe_through :api
  end
end
