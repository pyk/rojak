defmodule RojakAPI.Router do
  use RojakAPI.Web, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", RojakAPI do
    pipe_through :api

    scope "/v1", V1, as: :v1 do
      get "/", IndexController, :index
      get "/pairings", PairingController, :index
      get "/pairings/:id", PairingController, :show
      get "/candidates", CandidateController, :index
      get "/candidates/:id", CandidateController, :show
      get "/news", NewsController, :index
      get "/news/:id", NewsController, :show
      get "/media", MediaController, :index
      get "/media/:id", MediaController, :show
      get "/stats", StatsController, :index
    end
  end
end
