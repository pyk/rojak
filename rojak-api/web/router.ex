defmodule RojakAPI.Router do
  use RojakAPI.Web, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", RojakAPI do
    pipe_through :api

    get "/", IndexController, :index

    scope "/v1", V1, as: :v1 do
      get "/pairings", PairingController, :index
      get "/pairings/:id", PairingController, :show
      get "/pairings/:id/media-sentiments", PairingController, :media_sentiments
      get "/candidates", CandidateController, :index
      get "/candidates/:id", CandidateController, :show
      get "/candidates/:id/media-sentiments", CandidateController, :media_sentiments
      get "/news", NewsController, :index
      get "/news/:id", NewsController, :show
      get "/media", MediaController, :index
      get "/media/:id", MediaController, :show
      get "/media/:id/sentiments", MediaController, :sentiments
    end
  end
end
