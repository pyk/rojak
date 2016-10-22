defmodule RojakAPI.V1.MediaController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Media

  def index(conn, params) do
    limit = Dict.get(params, "limit", 10)
    offset = Dict.get(params, "offset", 0)
    media = Repo.all(
      from Media,
        limit: ^limit,
        offset: ^offset
    )
    render(conn, "index.json", media: media)
  end

  def show(conn, %{"id" => id}) do
    media = Repo.get!(Media, id)
    render(conn, "show.json", media: media)
  end

end
