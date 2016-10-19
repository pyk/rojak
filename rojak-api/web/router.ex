defmodule RojakAPI.Router do
  use RojakAPI.Web, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", RojakAPI do
    pipe_through :api

    get "/", IndexController, :index

    scope "/v1", V1, as: :v1 do
      get "/media", MediaController, :index
      get "/media/:id", MediaController, :show
    end
  end
end
