defmodule RojakAPI.V1.NewsView do
  use RojakAPI.Web, :view

  def render("index.json", %{news: news}) do
    render_many(news, RojakAPI.V1.NewsView, "news.json")
  end

  def render("show.json", %{news: news}) do
    render_one(news, RojakAPI.V1.NewsView, "news.json")
  end

  def render("news.json", %{news: news}) do
    Map.drop news, [:__meta__, :media, :sentiments, :mentions]
  end
end
