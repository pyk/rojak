defmodule RojakAPI.IndexController do
  use RojakAPI.Web, :controller

  def index(conn, _params) do
    render conn, "index.json"
  end
end
