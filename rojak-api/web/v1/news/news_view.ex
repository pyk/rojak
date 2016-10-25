defmodule RojakAPI.V1.NewsView do
  use RojakAPI.Web, :view

  def render("index.json", %{news: news}) do
    render_many(news, RojakAPI.V1.NewsView, "news.json")
  end

  def render("show.json", %{news: news}) do
    render_one(news, RojakAPI.V1.NewsView, "news.json")
  end

  def render("news.json", %{news: news}) do
    news =
      news
      |> Map.drop([:__meta__, :media, :sentiments, :mentioned_candidates])

    # Embed mentions
    news = case Map.get(news, :mentions) do
      %Ecto.Association.NotLoaded{} ->
        news |> Map.drop([:mentions])
      mentions ->
        Map.update! news, :mentions, fn _ ->
          Enum.map mentions, fn mention ->
            Map.drop(mention, [:__meta__, :mentioned_in, :sentiments])
          end
        end
    end

    news
  end
end
