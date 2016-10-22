defmodule RojakAPI.V1.NewsController do
  use RojakAPI.Web, :controller

  alias RojakAPI.News

  # TODO: also load mentions if `embed` parameter is set

  def index(conn, _params) do
    news = Repo.all(News)
    render(conn, "index.json", news: news)
  end

  def show(conn, %{"id" => id}) do
    news = Repo.get!(News, id)
    render(conn, "show.json", news: news)
  end

end
