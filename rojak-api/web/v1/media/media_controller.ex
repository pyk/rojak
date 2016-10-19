defmodule RojakAPI.V1.MediaController do
  use RojakAPI.Web, :controller

  alias RojakAPI.Media

  def index(conn, _params) do
    media = Repo.all(Media)
    render(conn, "index.json", media: media)
  end

  def show(conn, %{"id" => id}) do
    media = Repo.get!(Media, id)
    render(conn, "show.json", media: media)
  end

end
