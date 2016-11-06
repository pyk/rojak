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
      |> Map.drop([:__meta__, :media, :mentions])

    sentiments = Map.get(news, :sentiments)

    news =
      news
      |> Map.drop([:sentiments])

    # Embed mentions
    news = case sentiments do
      %Ecto.Association.NotLoaded{} ->
        news
      _ ->
        sentiments =
          Enum.map sentiments, fn news_sentiment ->
            candidate =
              news_sentiment
              |> Map.get(:sentiment)
              |> Map.get(:candidate)
              |> Map.drop([:__meta__, :mentioned_in, :pairing, :sentiments])
            sentiment_name =
              news_sentiment
              |> Map.get(:sentiment)
              |> Map.get(:name)
            sentiment_type = case sentiment_name do
              "pro" <> _ -> "positive"
              "net" <> _ -> "neutral"
              "con" <> _ -> "negative"
            end
            score =
              news_sentiment
              |> Map.get(:score)
            Map.put candidate, :sentiment, %{
              type: sentiment_type,
              score: score
            }
          end

        Map.put news, :sentiments, sentiments
    end

    news
  end
end
